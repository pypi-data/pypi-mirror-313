"""Base Inoopa configuration for python Logging."""

from dotenv import load_dotenv

load_dotenv()
import os
import logging
import logging_loki
from typing import Literal
from datetime import datetime
from rich.logging import RichHandler
from queue import Queue

from inoopa_utils.utils.env_variables_helper import get_env_name


LoggingLevel = Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG"]


def create_logger(
    logger_name: str, logging_level: LoggingLevel | None = None, logs_dir_path: str = "./logs", pretty: bool = False
) -> logging.Logger:
    """
    Configure how logging should be done.

    :param logger_name: The logger name to return.
    :param logging_level: The level of logging to filter. If none, will deduce from "ENV" env variable:
        'dev' will set logging_level to "DEBUG"
        'staging' will set logging_level to "INFO"
        'prod' will set logging_level to "INFO"
    :param logs_dir_path: The path to the logs directory.
    :param pretty: If True, will use rich to pretty print the logs. Only for development & CLI purpose.
    """
    if logging_level is None:
        logging_level = "DEBUG" if get_env_name() == "dev" else "INFO"

    # If the log directory doesn't exist, create it to avoid errors
    if not os.path.exists(logs_dir_path):
        os.makedirs(logs_dir_path, exist_ok=True)

    if pretty:
        handlers: list[logging.Handler] = [
            RichHandler(
                rich_tracebacks=True,
                show_path=False,
                show_time=False,
                show_level=True,
                log_time_format="[%X] ",
            )
        ]
    else:
        logs_format_formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)-8s %(name)-20s  |  %(message)s", datefmt="%d/%m/%Y %H:%M:%S"
        )
        # Write logs to file
        file_handler = logging.FileHandler(f"{logs_dir_path}/{datetime.now().strftime('%d-%m-%Y_%H:%M')}.log")
        file_handler.setFormatter(logs_format_formatter)
        file_handler.setLevel(logging_level)

        # Allow the logger to also log in console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logs_format_formatter)
        stream_handler.setLevel(logging_level)

        handlers = [stream_handler, file_handler]

    # If we are not in local dev, write logs to loki
    if not os.environ.get("LOCAL"):
        # get the service name
        app_name = " ".join(logger_name.split(".")[:2])
        # Write logs to loki our logs aggregator
        loki_handler = logging_loki.LokiQueueHandler(
            queue=Queue(-1),
            url="http://loki-gateway.monitoring.svc.cluster.local/loki/api/v1/push",
            version="1",
            tags={
                "App": app_name,
                "source": "inoopa-utils",
                "env": get_env_name(),
                "logger": logger_name,
                "language": "python",
            },
        )
        handlers.append(loki_handler)

    logger = logging.getLogger(logger_name)
    logger.handlers = handlers
    logger.setLevel(logging_level)

    return logger


if __name__ == "__main__":
    logger = create_logger("test_logger", logging_level="DEBUG", pretty=True)
    logger.info("test {'hello': 'world'}")
