import os

from sorted_markdown.parse import parse_markdown
from sorted_markdown.config import MARKDOWN_DIRECTORY, logger

if __name__ == "__main__":

    markdown_directory = os.listdir(MARKDOWN_DIRECTORY)
    logger.debug("markdown_directory: %s", markdown_directory)

    markdowns = list(map(parse_markdown, markdown_directory))
    sorted_metadata = sorted(markdowns, key=lambda item: item["datetime"], reverse=True)
    logger.debug("markdowns:\n%s", markdowns)
    logger.debug("sorted_markdowns:\n%s", sorted_metadata)
    