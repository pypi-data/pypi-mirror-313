from argparse import ArgumentParser, RawDescriptionHelpFormatter

from ..constants import CLI_DESCRIPTION, OPENI_LOGO_ASCII
from .dataset import DatasetCommands
from .model import ModelCommands
from .user import UserCommands


def main():
    parser = ArgumentParser(
        "openi",
        formatter_class=RawDescriptionHelpFormatter,
        description=OPENI_LOGO_ASCII + CLI_DESCRIPTION,
    )
    commands_parser = parser.add_subparsers()

    # Register commands
    UserCommands.register_subcommand(commands_parser)
    ModelCommands.register_subcommand(commands_parser)
    DatasetCommands.register_subcommand(commands_parser)

    # Let's go
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    # Run
    service = args.func(args)
    service.run()


if __name__ == "__main__":
    main()
