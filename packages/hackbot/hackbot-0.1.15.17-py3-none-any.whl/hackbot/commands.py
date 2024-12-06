import argparse
import asyncio
import json
import traceback
import os
from loguru import logger as log
from aiohttp.client_exceptions import ClientPayloadError
from hackbot.utils import get_version
from hackbot.hack import authenticate, cli_hack_target, generate_issues, get_selectable_models

__version__ = get_version()


def get_args() -> argparse.Namespace | int:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Hackbot - Eliminate bugs from your code")
    parser.add_argument("-v", "--version", action="version", version=f"GatlingX Hackbot v{__version__}")

    # General arguments
    parser.add_argument(
        "--address",
        default="https://app.hackbot.co",
        help="Hackbot service address",
    )
    parser.add_argument("--port", type=int, default=None, required=False, help="Service port number")
    parser.add_argument(
        "--api-key",
        default=os.getenv("HACKBOT_API_KEY"),
        help="API key for authentication (default: HACKBOT_API_KEY environment variable)",
    )

    subparsers = parser.add_subparsers(dest="command", help="What hackbot command to run", required=True)

    # Create the models command parser, empty but is a subcommand
    models_parser = subparsers.add_parser("models", help="Show the list of selectable models")

    # Create the run command parser
    run_parser = subparsers.add_parser("run", help="Run analysis on source code")
    run_parser.add_argument(
        "-s",
        "--source",
        default=".",
        help="Path to folder containing foundry.toml (default: current directory). If no foundry.toml is found, we search upwards from the specified directory.",
    )
    run_parser.add_argument("--output", help="Path to save analysis results")
    run_parser.add_argument("--auth-only", action="store_true", help="Only verify API key authentication")

    # The --profile argument (which cannot be used with the --model argument) specifies the profile to use
    run_parser.add_argument("--profile", type=str, default="pro", help="The profile to use (e.g. starter, pro) Default: pro")
    # The --model argument (which cannot be used with the --starter argument) requires the --starter argument to not be used, and specifies the model to use
    run_parser.add_argument(
        "--model",
        type=str,
        required=False,
        help="The backing LLM model to use (e.g. gpt-4o-mini, o1-mini, claude-3-5-sonnet etc.)",
    )

    # Hidden command for development, can send extra data to the server
    run_parser.add_argument("--debug", type=str, default=None, help=argparse.SUPPRESS)

    # Issue generation options
    issue_parser = run_parser.add_argument_group("Issue Generation Options")
    issue_parser.add_argument(
        "--issues_repo",
        type=str,
        help="The repository to generate issues in (format: username/repo). By default empty and so no issues are generated",
    )
    issue_parser.add_argument(
        "--github_api_key",
        type=str,
        required=False,
        help="GitHub API key for issue generation",
    )

    args = parser.parse_args()

    if args.command == "run":
        return check_run_args(args)

    return args


def check_run_args(args: argparse.Namespace) -> argparse.Namespace | int:
    """Check and validate commandline arguments for the run command."""

    # Find closest enclosing path with foundry.toml by searching upwards
    current_path = os.path.abspath(args.source)
    while current_path != os.path.abspath(os.sep):  # Stop at root, using os.sep for cross-platform
        if os.path.exists(os.path.join(current_path, "foundry.toml")):
            args.source = current_path
            break
        current_path = os.path.dirname(current_path)
    else:  # No foundry.toml found
        log.error(f"❌ Error: No foundry.toml found in {os.path.abspath(args.source)} or any parent directories")
        return 1
    args.source = current_path

    if not args.api_key:
        log.error("❌ Error: API key is required (either via --api-key or HACKBOT_API_KEY environment variable)")
        return 1

    # Check if the starter and model arguments were passed (not just set to default)
    if args.profile == "starter" and args.model:
        log.error(
            "❌ Error: Using the starter profile (--profile starter) and --model arguments together is not allowed, go to https://hackbot.co/pricing to upgrade your subscription"
        )
        return 1

    try:
        if args.debug is not None:
            args.debug = json.loads(args.debug)
    except Exception:
        log.info(f"❌ Error: Invalid debug argument / JSON parse error on debug string: {args.debug}")
        args.debug = None

    return args


def show_selectable_models(address: str, port: int, api_key: str) -> int:
    """Show the list of selectable models from the hackbot service."""
    try:
        response = asyncio.run(get_selectable_models(address, port, api_key))
    except Exception as e:
        log.error(f"❌ Error fetching selectable models: {traceback.format_exc()}")
        return 1
    log.info("Selectable models:")
    for model in response:
        log.info(f"  - {model}")
    return 0


def hackbot_run(args: argparse.Namespace) -> int:
    """Run the hackbot tool."""
    try:
        # Verify authentication
        if not asyncio.run(authenticate(args.address, args.port, args.api_key)):
            log.error("❌ Authentication failed")
            return 1

        log.info("✅ Authentication successful")

        if args.auth_only:
            return 0

        # Invocation get passed through to the api
        invocation_args = {
            "model": args.model if args.model else "",
            "profile": args.profile,
        }
        if args.debug is not None:
            log.info(f"Debug mode, sending (flat, since only using http forms): {args.debug}")
            for key, value in args.debug.items():
                invocation_args[key] = value

        # Perform the analysis
        results = asyncio.run(cli_hack_target(invocation_args, args.address, args.port, args.api_key, args.source, args.output))

        if args.issues_repo and results:
            log.info(f"Generating issues report on repo {args.issues_repo}")
            asyncio.run(generate_issues(args.issues_repo, args.github_api_key, results))
        else:
            log.debug("No github repository for reporting issues has been specified. Skipping github issue generation.")

        # Output results to output-path
        if args.output and results:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

        return 0

    except ClientPayloadError:
        log.error(
            "❌ The server terminated the connection prematurely, most likely due to an error in the scanning process. Check the streamed logs for error messages. Support: support@gatlingx.com"
        )
        return 1
    except Exception as e:
        if str(e) == "Hack request failed: 413":
            log.error("❌ The source code directory is too large to be scanned. Must be less than 256MB.")
        else:
            log.error(f"❌ Error: {str(e)}")
        return 1
