# command-sniffer

Command-sniffer is a python package that monitors the execution of an arbitrary
shell command. It can store the sub-command it executes (e.g. compilation commands
during the execution of the build command, e.g. `make`) and replay the command
history.

## Install

You will need to install the package before using it.

```shell
cd /path/to/command_interceptor
python3 -m pip install .
```

For developer installation, you can use the following command
to install the package.

```shell
cd /path/to/command_interceptor
python3 -m pip install -e . [dev]
```

And then you can use the command `intercept` ;)

# Usage
```shell
sniffcmd -o db.json -c /usr/bin/ls -- bash -c "ls"`
```
