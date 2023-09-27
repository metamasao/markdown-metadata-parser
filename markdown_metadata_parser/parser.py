import re
import os
from datetime import datetime

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
        metadata_dict = markdown_parser.parse()

        metadata = MarkdownMetadata(metadata_dict=metadata_dict, filename=filename)

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

    def parse(self):
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
        metadata_format_str.append("---")
        metadata_format_str.append(self.content_body)
        return "".join(metadata_format_str)


class MarkdownMetadata(dict):

    def __init__(self, metadata_dict, filename=None):
        super().__init__(metadata_dict)
        self.filename = filename
        self.datetime_data_added = False

    def __getitem__(self, key):
        item = super().__getitem__(key)
        return datetime.fromisoformat(item) if key == "created" or key == "updated" else item
    
    def __setitem__(self, key, item):
        if key == "created" or key == "updated":
            self.datetime_data_added = True
        super().__setitem__(key, item)
    
    def _update_metadata_with_datetime_data(self):
        is_datetime_data = ("created" in self) and ("updated" in self)
        if is_datetime_data:
            return False, self
        
        datetime_value = datetime.now().isoformat(" ", timespec="seconds")
        self["created"], self["updated"] = datetime_value, datetime_value
        return True, self

    @classmethod
    def create_metadata(cls, metadata_dict, filename=None):
        markdown_metadata = cls(metadata_dict, filename)
        updated, markdown_metadata = markdown_metadata._update_metadata_with_datetime_data()
        if updated:
            return markdown_metadata
        
        validated_datetime_format_list = list(
            map(_validate_datetime_format, [markdown_metadata.get("created"), markdown_metadata.get("updated")])
            )
        if None in validated_datetime_format_list: 
            raise DatetimeDataFormatIsIncorrect(
                f"Datetime format is incorrect {filename}.\nWrite metadata following the rule\n'yyyy-mm-dd hh:mm:ss'"
            )
        return markdown_metadata
        
def _validate_datetime_format(datetime_item):
    return  re.match(r"^(\d){4}-(\d){2}-(\d){2} (\d){2}:(\d){2}:(\d){2}$", datetime_item)
    