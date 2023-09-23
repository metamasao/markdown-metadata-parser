import re
import os
from datetime import datetime
from typing import Any

from exceptions import MetadataNotFoundError, DatetimeDataNotFoundError, DatetimeDataFormatIsIncorrect
from config import logger, MARKDOWN_DIRECTORY


def sorted_markdowns(markdown_dir):
    markdown_files = [f"{markdown_dir}/{filename}" for filename in os.listdir(markdown_dir)]
    markdown_metadata = list(map(create_markdown_metadata, markdown_files))
    return sorted(markdown_metadata, key=lambda item: item["created"], reverse=True)


def create_markdown_metadata(filename):
    with open(filename) as f:
        return MarkdownMetadata.create_metadata(filename, f.read())


class MarkdownMetadata(dict):

    def __getitem__(self, key):
        item = super().__getitem__(key)
        return datetime.fromisoformat(item) if key == "created" or key == "updated" else item
    
    def __missing__(self, key):
        value = "not defined"
        if not (key == "created" or key == "updated"): 
            self[key] = value
            return value
        
        value = datetime.now().isoformat(" ", timespec="seconds")
        self[key] = value
        return value

    @classmethod
    def create_metadata(cls, filename, content):
        check_is_metadata(filename, content)        
        content = parse_markdown(content)
        return cls(validate_metadata_datetime(content))
    

class MarkdownParser:
    
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

def check_is_metadata(filename, content):
    metadata = re.search(r"---(.+:.+)+---", content, re.DOTALL)
    if not metadata: raise MetadataNotFoundError(f"Metadata is not found in this {filename}")
    return True


def parse_markdown(content):
    metadata = content.split("---", maxsplit=2)[1]
    metadata = filter(lambda data: data != "", metadata.split("\n"))
    return {data.split(":")[0]: data.split(":", maxsplit=1)[1].lstrip() for data in metadata}


def validate_metadata_datetime(iterable):
    if re.match(r"^(\d){4}-(\d){2}-(\d){2} (\d){2}:(\d){2}:(\d){2}$", iterable["created"]) is None:
        raise DatetimeDataFormatIsIncorrect("Datetime format is incorrect.\nWrite metadata following the rule\n'yyyy-mm-dd hh:mm:ss'")
    return iterable