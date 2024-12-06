from hulu_evaluate.commands.config import get_config_parser
from hulu_evaluate.commands.submit import submit_command_parser
from hulu_evaluate.commands.utils import CustomArgumentParser
from hulu_evaluate.commands.login import login_command_parser
from hulu_evaluate.commands.train import train_command_parser


def main():
    parser = CustomArgumentParser("HuLU evaluate CLI tool", usage="hulu-evaluate <command> [<args>]", allow_abbrev=False)
    subparsers = parser.add_subparsers(help="hulu-evaluata command helpers")

    # Register commands
    get_config_parser(subparsers=subparsers)
    submit_command_parser(subparsers=subparsers)
    login_command_parser(subparsers=subparsers)
    train_command_parser(subparsers=subparsers)

    # Let's go
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    # Run
    args.func(args)


if __name__ == "__main__":
    main()