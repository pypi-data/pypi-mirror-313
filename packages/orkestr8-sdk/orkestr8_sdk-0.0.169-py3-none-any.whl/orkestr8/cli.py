from argparse import ArgumentParser

from orkestr8.commands.download_model import Destination


def _build_global_aws_option_parser():
    """Parent parser for AWS options to be specific"""
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--aws-access-key", nargs="?", action="store")
    parser.add_argument("--aws-secret-key", nargs="?", action="store")
    parser.add_argument("--aws-bucket-name", nargs="?", action="store")
    return parser


def _build_global_option_parser() -> ArgumentParser:
    "Parent parser to define optoins used for ALL commands"
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-y",
        dest="default_yes",
        action="store_true",
        help="Apply yes by default to all inputs",
    )
    parser.add_argument(
        "--generate-new-train-test",
        action="store_true",
        help="Generates new training and validation data. This is automatic"
        " if image data is add to the server",
    )

    return parser


def _build_file_location_parser() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--remote-file-path", nargs="?")
    parser.add_argument("--dest-file-path", nargs="?")
    return parser


def parse_args():
    """Builds 'main' parser"""
    all_option_parser = _build_global_option_parser()
    file_option_parser = _build_file_location_parser()
    aws_options_parser = _build_global_aws_option_parser()
    # This creates 'mutually' exclusive parsers
    parser = ArgumentParser(prog="Orchkestr8 ML train runner")
    subparsers = parser.add_subparsers(dest="command", help="Invocation commands")
    # This creates 'mutually' exclusive parsers

    train_parser = subparsers.add_parser(
        "train", help="Runs the training logic only", parents=[all_option_parser]
    )
    train_parser.add_argument(
        "model_module",
        action="store",
        help="The module that contains the model to run. Module MUST have a `run` method defined",
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Runs the data update and training logic",
        parents=[all_option_parser, file_option_parser, aws_options_parser],
    )
    run_parser.add_argument(
        "--model-module",
        action="store",
        help="The module that contains the model to run. Module MUST have a `run` method defined",
    )
    run_parser.add_argument(
        "--remote_file_path", help="Where to direct Orkestr8 to pull the file from"
    )
    run_parser.add_argument(
        "--dest_file_path", help="Where to direct Orkestr8 to write file path"
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Runs the data update function.",
        parents=[all_option_parser, aws_options_parser],
    )
    update_parser.add_argument(
        "remote_file_path", help="Where to direct Orkestr8 to pull the file from"
    )
    update_parser.add_argument(
        "dest_file_path", help="Where to direct Orkestr8 to write file path"
    )
    stop_parser = subparsers.add_parser(
        "stop", help="Invokes 'global' stop command to running process"
    )
    stop_parser.add_argument(
        "--pid",
        help="PID of Python process to shutdown. If not specificed Orkstr8 will automatically retreive PID",
    )
    subparsers.add_parser("poll", help="Retrieve data from the active process")

    download_model_parser = subparsers.add_parser(
        "download_model",
        help="Download the trained weights of the model",
        parents=[aws_options_parser],
    )
    download_model_parser.add_argument(
        "to", help="Location to save the model", choices=Destination._member_names_
    )
    download_model_parser.add_argument(
        "--model-location", help="Location of .pth file", required=True
    )
    download_model_parser.add_argument(
        "--remote-location",
        help="File path to place model of 'to' argument",
        required=True,
    )
    check_parser = subparsers.add_parser(
        "check", help="Checks running state of training session"
    )
    check_parser.add_argument(
        "--file",
        help=(
            "File which contains process information. If file can be accessed AND has PID value"
            + ", will return ACTIVE, else INACTIVE for all other scenarios"
        ),
    )
    subparsers.add_parser("mock_run", help="Invokes a false training scenario")
    return parser.parse_args()
