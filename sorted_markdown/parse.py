import re
from datetime import datetime

from sorted_markdown.exceptions import MetadataNotFoundError
from sorted_markdown.config import logger, MARKDOWN_DIRECTORY


def parse_markdown(filename):
    with open(f"{MARKDOWN_DIRECTORY}/{filename}") as f:
        content = f.read()
        check_is_metadata(content)
        return get_basic_metadata(content)

def get_basic_metadata(content):
    metadata = content.split("---", maxsplit=2)[1]
    metadata = {
        data.split(":")[0]: data.split(":", maxsplit=1)[1].lstrip() for data in metadata.split("\n") if data != ""
    }
    return DictForSortedMetadata(metadata)

def check_is_metadata(content):
    metadata = re.search("(-){3}", content)
    if not metadata: raise MetadataNotFoundError("Metadata is not found in a markdown file.")
    return True


class DictForSortedMetadata(dict):

    def __getitem__(self, key):
        item = super().__getitem__(key)
        return datetime.fromisoformat(item) if key == "datetime" else item
