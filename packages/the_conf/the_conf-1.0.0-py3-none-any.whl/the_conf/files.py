import json
import logging
from os.path import abspath, expanduser, splitext
from typing import Union, Optional, Tuple, Generator
import yaml

from the_conf.utils import Index
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# from Crypto.Random import get_random_bytes


logger = logging.getLogger(__name__)
ENCODING = "utf8"
CRYPT_SEPARATOR = ";"


def decrypt(
    payload: str,
    passkey: Union[bytes, str],
    separator: str = CRYPT_SEPARATOR,
) -> str:
    if isinstance(passkey, str):
        passkey = passkey.encode(ENCODING)
    assert len(passkey) >= 32, "Your passkey is too short"
    nonce, data, tag, *_meta = payload.split(separator)
    if nonce and data:
        cipher = AES.new(passkey, AES.MODE_GCM, nonce=b64decode(nonce))
        try:
            return cipher.decrypt_and_verify(
                b64decode(data), b64decode(tag)
            ).decode(ENCODING)
        except ValueError:
            pass
    raise RuntimeError("Couldn't decrypt payload")


def encrypt(
    payload: str,
    passkey: Union[bytes, str],
    separator: str = CRYPT_SEPARATOR,
) -> str:
    if isinstance(passkey, str):
        passkey = passkey.encode(ENCODING)
    assert len(passkey) >= 32, "Your passkey is too short"
    nonce = get_random_bytes(12)
    cipher = AES.new(passkey, AES.MODE_GCM, nonce=nonce)
    data, tag = cipher.encrypt_and_digest(payload.encode(ENCODING))

    crypted_payload = [
        b64encode(nonce).decode(ENCODING),
        b64encode(data).decode(ENCODING),
        b64encode(tag).decode(ENCODING),
    ]
    return separator.join(crypted_payload)


def read(
    paths, passkey: Optional[str] = None
) -> Generator[Tuple[str, str], None, None]:
    any_found = False
    for path in paths:
        path = abspath(expanduser(path.strip()))
        ext = splitext(path)[1][1:]
        try:
            with open(path, "r", encoding=ENCODING) as fd:
                payload = fd.read().strip()
                if passkey is not None:
                    try:
                        payload = decrypt(payload, passkey)
                    except RuntimeError:
                        pass
                if ext in {"yml", "yaml"}:
                    yield path, yaml.load(payload, Loader=yaml.FullLoader)
                elif ext == "json":
                    yield path, json.load(fd)
                else:
                    logger.error(
                        "File %r ignored: unknown type (%s)", path, ext
                    )
                    continue
            any_found = True
        except FileNotFoundError:
            logger.debug("%r not found", path)
        except PermissionError:
            logger.warning("%r: no right to read", path)
    if not any_found:
        logger.warning("no file found among %r", paths)


def extract_value(config, path, full_path=None):
    full_path = full_path or []
    if len(path) == 1 and path[0] in config:
        yield full_path + [path[0]], config[path[0]]
    elif path[0] is Index and isinstance(config, (list, tuple)):
        for index, sub_config in enumerate(config):
            if len(path) == 1:
                yield full_path + [index], sub_config
            else:
                yield from extract_value(
                    config[index], path[1:], full_path + [index]
                )
    elif path[0] in config:
        yield from extract_value(
            config[path[0]], path[1:], full_path + [path[0]]
        )
    else:
        raise ValueError(f"no {path[0]!r} in {config!r}")


def extract_values(paths, config, config_file):
    for path in paths:
        try:
            if Index in path:
                for full_path, sub_value in extract_value(config, path):
                    yield full_path, sub_value
            else:
                for full_path, value in extract_value(config, path):
                    assert full_path == path
                    yield path, value
        except ValueError:
            logger.debug("%s not found in %r", ".".join(path), config_file)


def write(config, path):
    path = abspath(expanduser(path.strip()))
    ext = splitext(path)[1][1:]
    if ext in {"yml", "yaml"}:
        with open(path, "w", encoding=ENCODING) as fp:
            yaml.dump(config, fp)
    elif ext == "json":
        with open(path, "w", encoding=ENCODING) as fp:
            json.dump(config, fp)
    else:
        raise ValueError(
            "couldn't make out file type, conf file path should "
            "end with either yml, yaml or json"
        )
