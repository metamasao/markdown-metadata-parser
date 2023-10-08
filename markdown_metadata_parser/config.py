import os
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
    if (spec := importlib.util.find_spec("config")) is None:
        logger.info(
            """
            config.py is not found in your project directory.
            Please create 'config.py' file 
            and specify markwodn directory and metadata directory.
            """
        )
    config_module = importlib.util.module_from_spec(spec=spec)
    spec.loader.exec_module(config_module)
    return config_module

config_in_project_directory = get_config()    
markdown_directory = config_in_project_directory.MARKDOWN_DIRECTORY
metadata_directory = config_in_project_directory.METADATA_DIRECTORY
