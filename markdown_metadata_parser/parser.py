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
    with open(filename, mode="+") as f:
        markdown_parser = MarkdownParser(filename=filename, content=f.read())
        markdown_parser.has_metadata()
        metadata_dict = markdown_parser.parse_markdown()

        metadata = MarkdownMetadata(metadata_dict=metadata_dict, filename=filename)
        metadata.validate_metadata_datetime()

        # if metadata.datetime_data_added:
        #     f.write()
        return metadata


class MarkdownParser:
    
    def __init__(self, content, filename=None):
        self.filename = filename
        self.content = content
        self.content_body = None

    def has_metadata(self):
        metadata = re.search(r"---(.+:.+)+---", self.content, re.DOTALL)
        if not metadata: raise MetadataNotFoundError(f"Metadata is not found in this {self.filename}")
        return True

    def parse_markdown(self):
        content = self.content.split("---", maxsplit=2)
        metadata = content[1]
        self.content_body = content[2]
        
        metadata_dict = filter(lambda data: data != "", metadata.split("\n"))
        metadata_dict = {data.split(":")[0]: data.split(":", maxsplit=1)[1].lstrip() for data in metadata_dict}
        return metadata_dict
    
    def concatenate_new_metadata_and_content_body(self, new_metadata):
        from collections import deque

        metadata_format_str = deque([f"{key}: {item}\n" for key, item in new_metadata.items()])
        metadata_format_str.appendleft("---\n")
        metadata_format_str.append("---\n")
        metadata_format_str.append(self.content_body)
        return "".join(metadata_format_str)


class MarkdownMetadata(dict):

    def __init__(self, metadata_dict, filename=None):
        super().__init__(metadata_dict)
        self.filename = filename
        self.datetime_data_added = False

    def __getitem__(self, key):
        item = super().__getitem__(key)
        if not(key == "created" or key == "updated"):
            return item
        
        datetime_item = self._validate_metadata_datetime(datetime_item=item)
        return datetime.fromisoformat(datetime_item)
    
    def __setitem__(self, key, item):
        if key == "created" or key == "updated":
            self.datetime_data_added = True
        super().__setitem__(key, item)

    def __missing__(self, key):
        value = "not defined"
        if not (key == "created" or key == "updated"): 
            self[key] = value
            return value
        
        value = datetime.now().isoformat(" ", timespec="seconds")
        self[key] = value
        return value
    
    def _validate_metadata_datetime(self, datetime_item):
        if re.match(r"^(\d){4}-(\d){2}-(\d){2} (\d){2}:(\d){2}:(\d){2}$", datetime_item) is None:
            raise DatetimeDataFormatIsIncorrect(
            f"Datetime format {datetime_item} is incorrect {self.filename}.\nWrite metadata following the rule\n'yyyy-mm-dd hh:mm:ss'"
            )
        return datetime_item
    