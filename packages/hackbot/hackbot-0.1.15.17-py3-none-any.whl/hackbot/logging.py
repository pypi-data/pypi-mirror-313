from tqdm import tqdm
from typing import Any
from loguru import logger as log


def loguru_file_formatter(record: Any) -> str:
    # Escape any curly braces in the message to prevent formatting errors
    message = str(record["message"]).replace("{", "{{").replace("}", "}}")
    return (
        f"<green>{record['time']:YYYY-MM-DD HH:mm:ss} </green> "
        f"({record['elapsed'].total_seconds():>7.2f}s) | "
        f"<level>{record['level']: <8}</level> | "
        f"- <level>{message}</level>\n"
    )


def loguru_progress_formatter(record: Any) -> str:
    # Escape any curly braces in the message to prevent formatting errors
    message = str(record["message"]).replace("{", "{{").replace("}", "}}")
    return f"<green>{record['time']:HH:mm:ss} </green> " f"({record['elapsed'].total_seconds():>5.1f}s) | " f"- <level>{message}</level>\n"


def setup_loguru():
    """Configure and return a logger instance with task-specific session ID"""
    # Remove default handlers
    log.remove()

    log.add(
        "hackbot.log",
        format=loguru_file_formatter,
        level="INFO",
        rotation="100kb",
        retention="10 days",
        backtrace=True,
    )
    log.add(
        lambda msg: tqdm.write(msg, end=""),
        colorize=True,
        format=loguru_progress_formatter,
        level="INFO",
    )
