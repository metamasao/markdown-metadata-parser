import re
import os
import logging

from .exceptions import MetadataNotFoundError

logger = logging.getLogger("markdown_metadata_parser.parser")


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
    
    def to_html(self):
        pass

    def wrap_content_with_tag(self, content, tag):
        pass

    def parse_content(self):
        pass

def _wrap_content_with_tag(content, tag):
    pass
    