import asyncio
import gzip
import json
import logging
import subprocess
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import TextIO

from pydantic import BaseModel

from connector.generated import CapabilityName as OpenApiCapabilityName
from connector.helpers import get_pydantic_model
from connector.oai.integration import Integration

now = datetime.utcnow()
daily_rotation = now.strftime("%Y-%m-%d")
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(logs_dir.joinpath(f"all_commands_{daily_rotation}.log")),
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Hacking commands
# ----------------


def _prep_hacking_command(args: Namespace):
    data = vars(args)
    data.pop("command")
    data.pop("func")
    return data


def http_integration_server(integration: Integration, port: int = 8000):
    from connector.http_server import collect_integration_routes, runserver

    router = collect_integration_routes(integration)
    try:
        runserver(router, port)
    except KeyboardInterrupt:
        pass


def build_executable(path: str) -> None:
    try:
        subprocess.run(["pyinstaller", "--version"], check=True)
    except FileNotFoundError:
        print("PyInstaller not found in PATH. Please pip install pyinstaller")
        return

    command = [
        "pyinstaller",
        path,
        "--noconsole",
        "--onefile",
        "--clean",
        "--paths=projects/libs/python/connector-sdk",
    ]
    if __file__ not in "site-packages":
        command.append("--paths=projects/libs/python/connector-sdk")
    subprocess.run(command)


def run_test():
    subprocess.run(["pytest", "tests/"], check=True)


def create_integration_hacking_parser(integration: Integration, parser: ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="command")

    http_server_parser = subparsers.add_parser("http-server")
    http_server_parser.add_argument(
        "--port", "-p", type=int, default=8000, help="The port to run the server on."
    )
    http_server_parser.set_defaults(
        func=lambda args: http_integration_server(integration, **_prep_hacking_command(args))
    )

    build_executable_parser = subparsers.add_parser(
        "build-executable",
        help=(
            "Create a single file executable with PyInstaller. Provide the path to your library's"
            " main.py file."
        ),
    )
    build_executable_parser.add_argument("path", type=str, help="The path to the main.py file.")
    build_executable_parser.set_defaults(
        func=lambda args: build_executable(**_prep_hacking_command(args))
    )

    test_parser = subparsers.add_parser("test")
    test_parser.set_defaults(func=lambda args: run_test())

    return None


# Actual Commands
# ---------------
PRINTABLE_OUTPUTS_T = BaseModel | str | dict | list


def _print_pydantic(model: PRINTABLE_OUTPUTS_T, file: TextIO | None = None):
    str_result = None
    # Pydantic v2
    if hasattr(model, "model_dump_json"):
        str_result = model.model_dump_json()
    # Pydantic v1
    elif hasattr(model, "json"):
        str_result = model.json()
    elif type(model) in (dict, list):
        str_result = json.dumps(model, sort_keys=True)
    else:
        str_result = str(model)

    if file:
        logger.info("compressing result")
        str_result_bytes = str_result.encode("utf-8")
        gzipped_result = gzip.compress(str_result_bytes)
        logger.info("writing compressed result to file")
        file.buffer.write(gzipped_result)
        logger.info("compressed result written to file")
        return
    else:
        print(str_result)


def get_result_file_path(args: Namespace) -> str | None:
    if not args.result_file_path:
        return None
    result_file_path = args.result_file_path.strip('"').strip("'")
    if not result_file_path.endswith(".gz"):
        raise ValueError("The result file name must end with the .gz extension.")
    return result_file_path


def capability_executor(integration: Integration, args: Namespace):
    """Executes a command from the CLI."""
    # validate that a valid gzip file name was provided
    result_file_path = get_result_file_path(args)

    output: PRINTABLE_OUTPUTS_T
    if args.command == "info":
        output = integration.info()
    else:
        output = asyncio.run(integration.dispatch(OpenApiCapabilityName(args.command), args.json))
    if result_file_path:
        logger.info(f"Attempting to open file name: {result_file_path}")
        with open(result_file_path, "w") as f:
            logger.info(f"File opened to write: {result_file_path}")
            _print_pydantic(output, f)
        logger.info(f"Result saved to {args.result_file_path}")
    else:
        logger.info("Result printing to console")
        _print_pydantic(output)
    logger.info("Command completed")


def collect_capabilities(integration: Integration, no_print: bool = False) -> ArgumentParser:
    """
    Collect all methods from an Integration class and create a CLI
    command for each.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparser = subparsers.add_parser("info", description=integration.info.__doc__)
    subparser.add_argument(
        "--result-file-path",
        type=str,
        help=(
            "The path to the file to save the result to. If this file already exists, its "
            "content will be overwritten. If not provided, the result will be printed to the "
            "console. The result file will be gzip compressed so the input file name should "
            "end with the .gz extension."
        ),
        default=None,
    )
    subparser.set_defaults(func=lambda args: capability_executor(integration, args))

    for capability_name, capability in integration.capabilities.items():
        subparser = subparsers.add_parser(capability_name.value, description=capability.__doc__)

        try:
            get_pydantic_model(capability.__annotations__)
        except ValueError:
            pass
        else:
            subparser.add_argument("--json", type=str, help="JSON input", required=True)
            subparser.add_argument(
                "--result-file-path",
                type=str,
                help=(
                    "The path to the file to save the result to. If this file already exists, "
                    "its content will be overwritten. If not provided, the result will be "
                    "printed to the console. The result file will be gzip compressed so the "
                    "input file name should end with the .gz extension."
                ),
                default=None,
            )

        subparser.set_defaults(func=lambda args: capability_executor(integration, args))

    hacking_subparser = subparsers.add_parser("hacking")
    create_integration_hacking_parser(integration, hacking_subparser)

    return parser


def run_integration(
    integration: Integration,
    no_print: bool = False,
) -> None:
    logger.info("Running command started at %s", datetime.now())
    try:
        """Run a command from the CLI, integration version."""
        parser = collect_capabilities(integration, no_print)
        args = parser.parse_args()
        logger.info("Command arguments: %s", args)
        args.func(args)
    except Exception as e:
        logger.error(
            f"Error running command exception class: {e.__class__.__name__} exception: {e}"
        )
        logger.error("Stack trace:", exc_info=True)
        raise e
    logger.info("Command completed at %s", datetime.now())
