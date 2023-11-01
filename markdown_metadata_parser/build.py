import os
import sys
import logging
from argparse import ArgumentParser

import base_config
from parser import MarkdownParser
from metadata import MarkdownMetadata

logger = logging.getLogger("markdown_metadata_parser.build")

markdowns = base_config.markdown_directory

def build():
    parser = ArgumentParser()
    parser.add_argument(
        "--new-project", 
        help="create a file for configuration to start a project",
        action="store_true"
    )
    parser.add_argument(
        "--make-template",
        help="create a markdown file based on a template file",
        action="store_true"
    )
    args = parser.parse_args()

    if args.new_project:
        logger.info("project has begun!")
        project_name = input("project name: ")
        return logger.info(project_name)
    if args.make_template:
        return logger.info("creating template!")
    
    _build()


def _start_new_project():
    # accept markdown and metadata directory name, using jinja template, passing them as parameter, creating config.py
    pass


def _build_template_markdown():
    pass


def _build():
    _markdowns = os.listdir(markdowns)
    metadata_directory = base_config.metadata_directory

    logger.debug(f"_markdowns: {_markdowns}")
    markdown_metadata = list(map(_build_markdown_metadata, _markdowns))
    metadata_sorted = sorted(markdown_metadata, lambda item: item["created"], reverse=True)

def _build_markdown_metadata(filename):
    logger.debug("filename: %s", filename)
    logger.info(f"markdowns: {markdowns}")
    with open(f"{markdowns}/{filename}") as f:
        content = f.read()
        logger.info(f"content: {content}")

        logger.debug(f"parsing a file...: {filename}")
        parser = MarkdownParser(content=content, filename=filename)
        parser.has_metadata()
        metadata_dict = parser.parse()

        logger.debug(f"creating metadata based on metadata_dict:\n{metadata_dict}")
        markdown_metadata = MarkdownMetadata.create_metadata(metadata_dict=metadata_dict)

        if markdown_metadata.datetime_data_added:
            new_content = parser.concatenate_new_metadata_and_content_body(new_metadata=markdown_metadata)
            logger.debug(f"new_content:\n{new_content}")

            # with open...

if __name__ == "__main__":
    logger.info(sys.path)
    build()
