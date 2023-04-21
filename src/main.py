"""This module contains the main code for EV3PathBot."""
import logging

from src.configs import get_config

log_file_append = get_config("log_file_append")
if not log_file_append:
    log_file_append = False

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: on file %(filename)s, on line %(lineno)d: %(message)s",
    filename="logs.log",
    filemode="w" if not log_file_append else "a",
)

logging.info(
    f"logging file mode is {'append' if log_file_append else 'write'}, you can change it in the config file"
)
