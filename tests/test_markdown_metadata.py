from unittest import TestCase
from datetime import datetime

from markdown_metadata_parser.parser import MarkdownMetadata
from markdown_metadata_parser.exceptions import DatetimeDataFormatIsIncorrect


class TestMarkdwonMetadata(TestCase):

    def test_str_to_datetime_when_getting_item(self):
        # arrange
        markdown_metadata = MarkdownMetadata(
            {"created": "2023-01-01 00:00:00", "update": "2023-02-02 00:00:00"}
        )

        # act
        created_value = markdown_metadata["created"]
        updated_value = markdown_metadata["updated"]

        # assert
        self.assertEqual(isinstance(created_value, datetime), True)
        self.assertEqual(isinstance(updated_value, datetime), True)

    def test_created_datetime_created_by_missing_method(self):
        # arrange
        markdown_metadata = MarkdownMetadata({})

        # act
        initial_created_value = "created" in markdown_metadata.keys()
        markdown_metadata["created"]
        after_created_value = "created" in markdown_metadata.keys()

        # assert
        self.assertEqual(initial_created_value, False)
        self.assertEqual(after_created_value, True)
    
    def test_updated_datetime_created_by_missing_method(self):
        # arrange
        markdown_metadata = MarkdownMetadata({})

        # act
        initial_updated_value = "updated" in markdown_metadata.keys()
        markdown_metadata["updated"]
        after_updated_value = "updated" in markdown_metadata.keys()

        # assert
        self.assertEqual(initial_updated_value, False)
        self.assertEqual(after_updated_value, True)

    def test_not_defined_created_by_missing_method(self):
        # arrange
        markdwon_metadata = MarkdownMetadata({})

        # act
        inital_value = "test" in markdwon_metadata.keys()
        item_value = markdwon_metadata["test"]
        after_value = "test" in markdwon_metadata.keys()

        # assert
        self.assertEqual(inital_value, False)
        self.assertEqual(after_value, True)
        self.assertEqual(item_value, "not defined")

    def test_validate_metadata_datetime_when_given_invalid_format(self):
        # arrange
        invalid_datetime_format_long = "2023-01-01 00:00:000"
        invalid_datetime_format_short = "2023-01-01 00:00:0"
        markdown_metadata = MarkdownMetadata({})
        
        # act        
        with self.assertRaises(DatetimeDataFormatIsIncorrect) as cm_long:
            markdown_metadata._validate_metadata_datetime(invalid_datetime_format_long)
        with self.assertRaises(DatetimeDataFormatIsIncorrect) as cm_short:
            markdown_metadata._validate_metadata_datetime(invalid_datetime_format_short)

        # assert
        self.assertEqual(isinstance(cm_long.exception, DatetimeDataFormatIsIncorrect), True)
        self.assertEqual(isinstance(cm_short.exception, DatetimeDataFormatIsIncorrect), True)