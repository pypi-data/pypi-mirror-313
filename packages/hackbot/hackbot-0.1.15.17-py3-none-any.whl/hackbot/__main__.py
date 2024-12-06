from hackbot.commands import get_args, hackbot_run, show_selectable_models
from hackbot.logging import setup_loguru
from loguru import logger as log


def _run():
    setup_loguru()
    args = get_args()
    # Error code from get_args
    if isinstance(args, int):
        exit(args)
    if args.command == "run":
        exit(hackbot_run(args))
    elif args.command == "models":
        exit(show_selectable_models(args.address, args.port, args.api_key))
    else:
        log.error(f"❌ Error: Invalid command: {args.command}")
        exit(1)


if __name__ == "__main__":
    _run()
