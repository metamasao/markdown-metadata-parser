import os
import logging

# ---------------markdown directory config-------------
cwd = os.getcwd()

MARKDOWN_DIRECTORY = f"{cwd}/markdowns"
MARKDOWN_METADATA_DIRECTORY = f"{cwd}/markdown_metadata"

# -----------------logging config----------------------
log_format = "%(asctime)s %(levelname)s %(filename)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)

logger = logging.getLogger()
