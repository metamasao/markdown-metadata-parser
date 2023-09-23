import re
import os
from datetime import datetime
from typing import Any

from markdown_metadata_parser.exceptions import MetadataNotFoundError, DatetimeDataNotFoundError, DatetimeDataFormatIsIncorrect
from markdown_metadata_parser.config import logger, MARKDOWN_DIRECTORY


def sorted_markdowns(markdown_dir):
    markdown_files = [f"{markdown_dir}/{filename}" for filename in os.listdir(markdown_dir)]
    markdown_metadata = list(map(create_markdown_metadata, markdown_files))
    return sorted(markdown_metadata, key=lambda item: (item["created"], item["updated"]), reverse=True)


def create_markdown_metadata(filename):
    with open(filename) as f:
        markdown_parser = MarkdownParser(filename=filename, content=f.read())
        markdown_parser.is_metadata()
        metadata_dict = markdown_parser.parse_markdown()

        metadata = MarkdownMetadata(metadata_dict=metadata_dict, filename=filename)
        return metadata.validate_metadata_datetime()


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
    
    def __init__(self, metadata_dict, filename=None):
        self.filename = filename
        super().__init__(metadata_dict)
    
    def validate_metadata_datetime(self):
        result = list(map(_validate_metadata_datetime, [self["created"], self["updated"]]))
        if None in result:
            raise DatetimeDataFormatIsIncorrect(
            f"Datetime format is incorrect {self.filename}.\nWrite metadata following the rule\n'yyyy-mm-dd hh:mm:ss'"
        )
        return self
    
def _validate_metadata_datetime(datetime_item):
    return re.match(r"^(\d){4}-(\d){2}-(\d){2} (\d){2}:(\d){2}:(\d){2}$", str(datetime_item))
        
    
class MarkdownParser:
    
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def is_metadata(self):
        metadata = re.search(r"---(.+:.+)+---", self.content, re.DOTALL)
        if not metadata: raise MetadataNotFoundError(f"Metadata is not found in this {self.filename}")
        return True

    def parse_markdown(self):
        metadata = self.content.split("---", maxsplit=2)[1]
        metadata = filter(lambda data: data != "", metadata.split("\n"))
        return {data.split(":")[0]: data.split(":", maxsplit=1)[1].lstrip() for data in metadata}
    
    def serialize(self):
        pass