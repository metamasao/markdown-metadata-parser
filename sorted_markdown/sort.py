import re
import os
from datetime import datetime

from exceptions import MetadataNotFoundError
from config import logger, MARKDOWN_DIRECTORY


def sorted_markdowns(markdown_dir):
    markdown_files = [f"{markdown_dir}/{filename}" for filename in os.listdir(markdown_dir)]
    markdown_metadata = list(map(create_markdown_metadata, markdown_files))
    return sorted(markdown_metadata, key=lambda item: item["datetime"], reverse=True)


def create_markdown_metadata(filename):
    with open(filename) as f:
        content = f.read()
        check_is_metadata(filename, content)
        return MarkdownMetadata.create_metadata(content)


def check_is_metadata(filename, content):
    metadata = re.search(r"---(.+:.+)+---", content, re.DOTALL)
    if not metadata: raise MetadataNotFoundError(f"Metadata is not found in this {filename}")
    return True


class MarkdownMetadata(dict):

    def __getitem__(self, key):
        item = super().__getitem__(key)
        return datetime.fromisoformat(item) if key == "datetime" else item

    @classmethod
    def create_metadata(cls, content):
        return cls(parse_markdown(content))
    

def parse_markdown(content):
    metadata = content.split("---", maxsplit=2)[1]
    metadata = filter(lambda data: data != "", metadata.split("\n"))
    return {data.split(":")[0]: data.split(":", maxsplit=1)[1].lstrip() for data in metadata}