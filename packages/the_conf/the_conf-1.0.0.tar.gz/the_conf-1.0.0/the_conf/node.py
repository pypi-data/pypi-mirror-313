import logging
from copy import deepcopy
from itertools import chain

from the_conf.utils import TYPE_MAPPING, Index, NoValue
from the_conf.files import extract_value

logger = logging.getLogger(__name__)


class AbstractNode:
    def __init__(self, parameters=None, parent=None, name=""):
        self._name = name
        self._parent = parent
        self._parameters = {}
        self._children = []
        self._load_parameters(parameters if parameters is not None else [])

    @property
    def _path(self):
        if self._parent is None:
            return []
        return self._parent._path + [self._name]

    def _get_path_val_param(self, absolute=True):
        raise NotImplementedError()

    def _set_to_path(self, path, value, overwrite=False):
        """Will set the value to the provided path. Local node if path length
        is one, a child node if path length is more that one.

        path: list
        value: the value to set
        """

    def _load_parameters(self, parameters):
        for parameter in parameters:
            node_type = parameter.get("type", "dict")
            node_type = TYPE_MAPPING.get(node_type) or node_type
            name = next(key for key in parameter if key != "type")
            is_node = isinstance(parameter[name], list)
            if node_type is dict:
                if is_node and not self._has_attr(name):
                    node = ConfNode(
                        parameters=parameter[name], name=name, parent=self
                    )
                    setattr(self, name, node)
                elif is_node:
                    getattr(self, name)._load_parameters(parameter[name])
                else:
                    self._load_parameter(name, parameter[name])
            elif node_type is list:
                if not self._has_attr(name):
                    node = ListNode(
                        parameters=parameter[name] if is_node else None,
                        node_type=None if is_node else parameter[name],
                        name=name,
                        parent=self,
                    )
                    setattr(self, name, node)
                else:
                    raise Exception("_load_parameters")
            if name not in self._children:
                self._children.append(name)

    def _load_parameter(self, name, settings, node_type=dict):
        if name in self._parameters:
            logger.debug("ignoring")
            return
        has_default = bool(settings.get("default"))
        has_type = bool(settings.get("type"))
        # something smarter that'd allow custom type
        if has_default and not has_type:
            settings["type"] = type(settings["default"])
        else:
            if settings.get("type") in TYPE_MAPPING:
                settings["type"] = TYPE_MAPPING[settings["type"]]
            elif isinstance(settings.get("type"), type):
                pass
            elif has_type:
                logger.warning("unknown type %r", settings["type"])
                settings["type"] = str
            else:
                settings["type"] = str
        has_among = bool(settings.get("among"))
        settings["required"] = bool(settings.get("required"))
        settings["read_only"] = bool(settings.get("read_only"))

        path = ".".join(map(str, chain(self._path, [name])))
        if has_among:
            assert isinstance(settings["among"], list), (
                f"parameters {path!r} configuration has wrong value for "
                "'among', should be a list, ignoring it"
            )
        if has_default and has_among:
            assert settings.get("default") in settings.get("among"), (
                f"default value for {path!r} is not among the "
                f"selectable values ({settings.get('among')!r}"
            )
        if has_default and settings["required"]:
            raise ValueError(
                f"{path!r} required parameter can't have default value"
            )

        if "type" in settings and "default" in settings:
            settings["default"] = settings["type"](settings["default"])
        self._parameters[name] = settings

    def _has_attr(self, attr):
        try:
            super().__getattribute__(attr)
            return True
        except AttributeError:
            return False


class ConfNode(AbstractNode):
    def _set_to_path(self, path, value, overwrite=False):
        attr = path[0]
        if len(path) == 1:
            if not overwrite and self._has_attr(attr):
                return
            read_only = None
            if self._parameters[attr].get("read_only"):
                # bypassing overwrite protection since we either:
                # - do not have that value in the first place
                # - overwrite has been activated
                read_only = self._parameters[attr].pop("read_only")
            res = setattr(self, attr, value)
            if read_only is not None:
                self._parameters[attr]["read_only"] = read_only
            return res
        return getattr(self, attr)._set_to_path(
            path[1:], value, overwrite=overwrite
        )

    def __getattribute__(self, name):
        """Return a parameter of the node if this one is defined.
        Its default value if it has one.
        """
        if name.startswith("_"):
            return super().__getattribute__(name)
        if "default" in self._parameters.get(name, {}):
            try:  # Trying to get attr, if AttributeError => is absent
                return super().__getattribute__(name)
            except AttributeError:
                return self._parameters[name]["default"]
        return super().__getattribute__(name)

    def __setattr__(self, key, value):
        if key.startswith("_") or isinstance(value, AbstractNode):
            return super().__setattr__(key, value)
        if key not in self._parameters:
            raise ValueError(f"{self._path} is not a registered conf option")
        if self._parameters[key].get("read_only"):
            raise AttributeError("attribute is in read only mode")
        if "among" in self._parameters[key]:
            if value not in self._parameters[key]["among"]:
                raise ValueError(
                    f"{self._path!r}: value {value!r} isn't "
                    f"in {self._parameters[key]['among']!r}"
                )
        if "type" in self._parameters[key]:
            value = self._parameters[key]["type"](value)
        return super().__setattr__(key, value)

    def _get_path_val_param(self, absolute=True):
        for child in self._children:
            if isinstance(getattr(self, child, None), AbstractNode):
                yield from getattr(self, child)._get_path_val_param()
            else:
                if absolute:
                    path = self._path + [child]
                else:
                    path = [child]
                yield path, getattr(self, child, NoValue), self._parameters[
                    child
                ]

    def __repr__(self):
        result = {"string": f"<{self.__class__.__name__}({{"}
        result["length"] = len(result["string"])
        old_loc, new_loc = [], []

        def spaces(index):
            if len(result["string"]) != result["length"]:
                return " " * (4 * index + result["length"])
            return ""

        def open_path(index, name):
            result["string"] += f"{spaces(index)}{name!r}: {{\n"

        def close_path(index):
            result["string"] += f"{spaces(index - 1)}}},\n"

        def add_key(index, name, value):
            result["string"] += f"{spaces(index)}{name!r}: {value!r},\n"

        for path, value, _ in self._get_path_val_param():
            new_loc = path[:-1]
            if new_loc != old_loc:
                diff_index = None
                for index, old_new in enumerate(zip(old_loc, new_loc)):
                    if old_new[0] != old_new[1]:
                        diff_index = index
                        break
                if diff_index is not None:
                    for index in range(len(old_loc), diff_index, -1):
                        close_path(index)
                    for index in range(diff_index, len(new_loc)):
                        open_path(index, new_loc[index])
                elif len(old_loc) > len(new_loc):  # we got out
                    for index in range(len(old_loc), len(new_loc), -1):
                        close_path(index)
                elif len(new_loc) > len(old_loc):  # we got in
                    for index in range(len(old_loc), len(new_loc)):
                        open_path(index, new_loc[index])
            add_key(len(new_loc), path[-1], value)
            old_loc = new_loc
        for index in range(len(old_loc), 0, -1):
            close_path(index)
        return result["string"] + ")>"


class ListNode(list, AbstractNode):
    def __init__(
        self,
        *args,
        parameters=None,
        parent=None,
        name="",
        node_type=None,
        **kwargs,
    ):
        AbstractNode.__init__(self, parameters, parent, name)
        list.__init__(self, *args, **kwargs)
        self._node_type = node_type or {}
        if self._children:
            parameters = [
                {child: self._parameters[child]} for child in self._children
            ]
            self._template_node = ConfNode(parameters, parent=self, name=Index)

    def _get_path_val_param(self, absolute=True):
        path = self._path
        if self._children:
            for child in self._children:
                if self:
                    for index, value in enumerate(self):
                        yield from value._get_path_val_param()
                else:
                    yield (
                        path + [Index, child],
                        NoValue,
                        self._parameters[child],
                    )
        else:
            if self:
                for index, value in enumerate(self):
                    yield path + [index], value, self._parameters
            else:
                yield path + [Index], self, self._parameters

    def __setitem__(self, index, value):
        if self._node_type.get("type"):
            if not isinstance(value, self._node_type["type"]):
                value = self._node_type["type"](value)
            return super().__setitem__(index, value)
        node = deepcopy(self._template_node)
        for path, _, _ in node._get_path_val_param(absolute=False):
            for _, sub_value in extract_value(value, path):
                node._set_to_path(path, sub_value)
        return super().__setitem__(index, node)

    def _set_to_path(self, path, value, overwrite=False):
        assert isinstance(path[0], int)
        if len(path) == 1 and not self._children:
            if len(self) <= path[0]:
                self.append(value)
            else:
                self[path[0]] = value
        else:
            if len(self) <= path[0]:
                node = deepcopy(self._template_node)
                self.append(node)
            self[path[0]]._set_to_path(path[1:], value, overwrite)
