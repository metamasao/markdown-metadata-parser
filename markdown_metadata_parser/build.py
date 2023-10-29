import os
import sys
from argparse import ArgumentParser

import base_config


def build():
    # print(base_config.markdown_directory)
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
        print("project has begun!")
    if args.make_template:
        print("creating template!")
    
    


def _build_new():
    # accept markdown and metadata directory name, using jinja template, passing them as parameter, creating config.py
    pass


def _build_add():
    pass


def _build_tags():
    pass


def _build_template_markdown():
    pass


if __name__ == "__main__":
    build()
