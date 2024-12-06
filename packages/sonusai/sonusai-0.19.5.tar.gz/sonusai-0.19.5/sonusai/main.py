"""sonusai

usage: sonusai [--version] [--help] <command> [<args>...]

The sonusai commands are:
    <This information is automatically generated.>

Aaware Sound and Voice Machine Learning Framework. See 'sonusai help <command>'
for more information on a specific command.

"""

import signal


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def main() -> None:
    from importlib import import_module
    from pkgutil import iter_modules

    from sonusai import commands_list

    plugins = {}
    plugin_docstrings = []
    for _, name, _ in iter_modules():
        if name.startswith("sonusai_") and not name.startswith("sonusai_asr_"):
            module = import_module(name)
            plugins[name] = {
                "commands": commands_list(module.commands_doc),
                "basedir": module.BASEDIR,
            }
            plugin_docstrings.append(module.commands_doc)

    from docopt import docopt

    from sonusai import __version__
    from sonusai.utils import add_commands_to_docstring
    from sonusai.utils import trim_docstring

    args = docopt(
        trim_docstring(add_commands_to_docstring(__doc__, plugin_docstrings)),
        version=__version__,
        options_first=True,
    )

    command = args["<command>"]
    argv = args["<args>"]

    import sys
    from os.path import join
    from subprocess import call

    import sonusai
    from sonusai import logger

    base_commands = sonusai.commands_list()
    if command == "help":
        if not argv:
            exit(call(["sonusai", "-h"]))  # noqa: S603, S607
        elif argv[0] in base_commands:
            exit(call(["python", f"{join(sonusai.BASEDIR, argv[0])}.py", "-h"]))  # noqa: S603, S607

        for data in plugins.values():
            if argv[0] in data["commands"]:
                exit(call(["python", f"{join(data['basedir'], argv[0])}.py", "-h"]))  # noqa: S603, S607

        logger.error(f"{argv[0]} is not a SonusAI command. See 'sonusai help'.")
        sys.exit(1)

    if command in base_commands:
        exit(call(["python", f"{join(sonusai.BASEDIR, command)}.py", *argv]))  # noqa: S603, S607

    for data in plugins.values():
        if command in data["commands"]:
            exit(call(["python", f"{join(data['basedir'], command)}.py", *argv]))  # noqa: S603, S607

    logger.error(f"{command} is not a SonusAI command. See 'sonusai help'.")
    sys.exit(1)


if __name__ == "__main__":
    main()
