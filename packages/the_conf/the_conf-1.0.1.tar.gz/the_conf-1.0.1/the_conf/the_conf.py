import logging
import os

from the_conf import command_line, files, interractive, node, utils

logger = logging.getLogger(__name__)
DEFAULT_ORDER = "cmd", "files", "env"
DEFAULT_CONFIG_FILE_CMD_LINE = "-C", "--config"
DEFAULT_CONFIG_FILE_ENVIRON = ("THECONF_FILE",)
DEFAULT_PASSKEY_CMD_LINE = "-P", "--passkey"
DEFAULT_PASSKEY_ENVIRON = ("THECONF_PASSKEY",)


class TheConf(node.ConfNode):
    def __init__(
        self, *metaconfs, prompt_values=False, cmd_line_opts=None, environ=None
    ):
        self._source_order = list(DEFAULT_ORDER)
        self._config_files = []
        self._config_file_cmd_line = list(DEFAULT_CONFIG_FILE_CMD_LINE)
        self._config_file_environ = list(DEFAULT_CONFIG_FILE_ENVIRON)
        self._passkey_cmd_line = list(DEFAULT_PASSKEY_CMD_LINE)
        self._passkey_environ = list(DEFAULT_PASSKEY_ENVIRON)
        self._main_conf_file = None
        self._cmd_line_opts = cmd_line_opts
        self._environ = environ
        self._prompt_values = prompt_values
        self._passkey = None

        def is_default(value, default):
            if not value or isinstance(value, tuple):
                return True
            return tuple(value) == default

        def set_metaconf_setting(key, metaconf, default):
            if key not in metaconf:
                return
            new_value = metaconf[key]
            if isinstance(metaconf[key], (list, tuple, set)):
                new_value = list(new_value)
            elif isinstance(new_value, (str, int, float)):
                raise TypeError(
                    f"metaconf parameter {key} is "
                    f"of unknown type {type(new_value)!r}"
                )
            value = getattr(self, "_" + key)
            if is_default(value, default):
                setattr(self, "_" + key, new_value)
            else:
                value.extend(new_value)

        super().__init__()
        for mc in metaconfs:
            if isinstance(mc, str):
                _, mc = next(files.read([mc]))
            set_metaconf_setting("source_order", mc, DEFAULT_ORDER)
            set_metaconf_setting(
                "config_file_cmd_line", mc, DEFAULT_CONFIG_FILE_CMD_LINE
            )
            set_metaconf_setting(
                "config_file_environ", mc, DEFAULT_CONFIG_FILE_ENVIRON
            )
            set_metaconf_setting(
                "passkey_cmd_line", mc, DEFAULT_PASSKEY_CMD_LINE
            )
            set_metaconf_setting(
                "passkey_environ", mc, DEFAULT_PASSKEY_ENVIRON
            )
            set_metaconf_setting("config_files", mc, None)

            self._load_parameters(mc["parameters"])
        self.load()

    def _load_files(self):
        if self._config_files is None:
            return
        for conf_file, config in files.read(self._config_files, self._passkey):
            paths = list(path for path, _, _ in self._get_path_val_param())
            for path, value in files.extract_values(paths, config, conf_file):
                self._set_to_path(path, value, overwrite=True)

    def _load_cmd(self, opts=None):
        gen = command_line.yield_values_from_cmd(
            list(self._get_path_val_param()),
            self._cmd_line_opts,
            self._config_file_cmd_line,
            self._passkey_cmd_line,
        )
        config_file = next(gen)
        if config_file:
            self._config_files.insert(0, config_file)
        passkey = next(gen)
        if passkey:
            self._passkey = passkey

        for path, value in gen:
            self._set_to_path(path, value, overwrite=True)

    def _load_env(self, environ=None):
        if environ is None:
            environ = os.environ
        for config_env_key in self._config_file_environ:
            if config_env_key in environ:
                self._config_files.insert(0, environ[config_env_key])
        for passkey_env_key in self._passkey_environ:
            if passkey_env_key in environ:
                self._passkey = environ[passkey_env_key]
        for path, _, _ in self._get_path_val_param():
            env_key = "_".join(map(str.upper, path))
            if env_key in environ:
                self._set_to_path(path, environ[env_key], overwrite=True)

    def load(self):
        for order in self._source_order:
            if order == "files":
                self._load_files()
            elif order == "cmd":
                self._load_cmd(self._cmd_line_opts)
            elif order == "env":
                self._load_env(self._environ)
            else:
                raise ValueError(f"unknown order {order!r}")

        if self._prompt_values:
            self.prompt_values(False, False, False, False)

        for path, value, param in self._get_path_val_param():
            if value is utils.NoValue and param.get("required"):
                raise ValueError(
                    f"loading finished and {'.'.join(path)!r} " "is not set"
                )

    def _extract_config(self):
        config = {}
        for paths, value, param in self._get_path_val_param():
            if value is utils.NoValue:
                continue
            if "default" in param and value == param["default"]:
                continue
            curr_config = config
            for path in paths[:-1]:
                curr_config[path] = {}
                curr_config = curr_config[path]
            curr_config[paths[-1]] = value
        return config

    def write(self, config_file=None):
        if config_file is None and not self._config_files:
            raise ValueError("no config file to write in")

        files.write(
            self._extract_config(), config_file or self._config_files[0]
        )

    def prompt_values(
        self,
        only_empty=True,
        only_no_default=True,
        only_required=True,
        only_w_help=True,
    ):
        for path, value, param in self._get_path_val_param():
            if only_w_help and not param.get("help_txt"):
                continue
            if only_required and not param.get("required"):
                continue
            if only_no_default and not param.get("default"):
                continue
            if only_empty and value is not utils.NoValue:
                continue
            if param.get("type") is bool:
                self._set_to_path(
                    path,
                    interractive.ask_bool(
                        param.get("help_txt", ".".join(path)),
                        default=param.get("default"),
                        required=param.get("required"),
                    ),
                )
            else:
                self._set_to_path(
                    path,
                    interractive.ask(
                        param.get("help_txt", ".".join(path)),
                        choices=param.get("among"),
                        default=param.get("default"),
                        required=param.get("required"),
                        cast=param.get("type"),
                    ),
                )
