from loguru import logger
import os
import sys


def get_configured_logger(
    log_dir="logs",
    minimum_log_level="DEBUG",  # Renamed parameter
    log_format=None,
    sinks=None,
):
    """
    Initializes and returns a configured Loguru logger.

    :param log_dir: Directory for log files (default is "logs").
    :param minimum_log_level: Minimum log level to capture (default is "DEBUG").
    :param log_format: Log format string (optional). If not provided, a default format will be used.
    :param sinks: List of custom sinks to log to (optional). If not provided, default sinks (stdout and file) will be used.
    :return: Configured logger instance.
    """

    # Default log format if none is provided
    if log_format is None:
        log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Default sinks (stdout and log file)
    default_sinks = [
        {"sink": sys.stdout, "level": minimum_log_level, "format": log_format},
        {
            "sink": os.path.join(log_dir, "solugenerics.log"),
            "level": minimum_log_level,
            "format": log_format,
        },
    ]

    # Use custom sinks if provided, otherwise use the default sinks
    sinks = sinks if sinks is not None else default_sinks

    # Add sinks to the logger
    for sink in sinks:
        logger.add(
            sink["sink"],
            level=sink["level"],
            format=sink["format"],
        )

    return logger
