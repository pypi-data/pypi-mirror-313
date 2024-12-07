from . import TheConf, files

metaconf = {
    "source_order": ["cmd"],
    "parameters": [
        {"mode": {"type": str, "among": ["encrypt", "decrypt"]}},
        {
            "file": {
                "required": True,
                "type": str,
                "help": "path to the file to encrypt or decrypt",
            }
        },
        {
            "key": {
                "required": True,
                "type": str,
                "help": "the pass key to encrypt or decrypt file",
            }
        },
        {"encoding": {"default": "utf8"}},
    ],
}
cmdline = TheConf(metaconf)


def main():
    with open(cmdline.file, "r", encoding=cmdline.encoding) as fd:
        if cmdline.mode == "decrypt":
            content = files.decrypt(fd.read(), cmdline.key)
        else:
            content = files.encrypt(fd.read(), cmdline.key)

    with open(cmdline.file, "w", encoding=cmdline.encoding) as fd:
        fd.write(content)


if __name__ == "__main__":
    main()
