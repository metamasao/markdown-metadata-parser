import sys

from markdown_metadata_parser.parser import sorted_markdowns


def build():
    print(sys.argv[1])


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
    print(sorted_markdowns("../markdowns"))
