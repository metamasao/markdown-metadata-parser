import re
from datetime import datetime

from exceptions import DatetimeDataFormatIsIncorrect


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