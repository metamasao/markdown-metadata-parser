import os
import sys
import importlib.util
import logging


# -----------------logging config----------------------
logger = logging.getLogger("markdown_metadata_parser")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s")
)

logger.addHandler(console_handler)

# ---------------markdown directory config-------------
def get_config():
    spec = importlib.util.spec_from_file_location("config", f"{os.getcwd()}/config.py")
    config_module = importlib.util.module_from_spec(spec=spec)
    try:
        spec.loader.exec_module(config_module)
    except FileNotFoundError as err:
        logger.info("config.py is not found in your project directory.", exc_info=err)
        sys.exit()
    return config_module

config_in_project_directory = get_config()   
markdown_directory = config_in_project_directory.MARKDOWN_DIRECTORY
metadata_directory = config_in_project_directory.METADATA_DIRECTORY
