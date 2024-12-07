import logging
import logging.config
import logging.handlers
from pathlib import Path

import yaml


def setup_logging(logconfigpath : str):
    if not logconfigpath:
        logconfigpath = "palcodeinfra/logging-config.yml";
    
    logging_config_file = Path(logconfigpath)
    with open(logging_config_file, "r") as f:
        logging_config = yaml.safe_load(f)

    logging.config.dictConfig(logging_config)


def get_logger(loggername : str):
    return logging.getLogger(loggername)