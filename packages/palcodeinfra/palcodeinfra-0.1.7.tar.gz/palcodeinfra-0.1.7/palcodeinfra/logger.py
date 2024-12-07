import logging
import logging.config
import logging.handlers
from pathlib import Path

import yaml

def get_logger(name : str, configpath : str = None):
    if not configpath:
        configpath = "palcodeinfra/logging-config.yml";
    
    logging_config_file = Path(configpath)
    with open(logging_config_file, "r") as f:
        logging_config = yaml.safe_load(f)

    logging.config.dictConfig(logging_config)
    return logging.getLogger(name)