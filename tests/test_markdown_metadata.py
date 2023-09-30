from unittest import TestCase
from datetime import datetime

from markdown_metadata_parser.metadata import MarkdownMetadata, _validate_datetime_format
from markdown_metadata_parser.exceptions import DatetimeDataFormatIsIncorrect


class TestMarkdwonMetadata(TestCase):

    def test__getitem__str_to_datetime_when_getting_item(self):
        # arrange
        markdown_metadata = MarkdownMetadata(
            {
                "created": "2023-01-01 00:00:00", 
                "updated": "2023-02-02 00:00:00"
            }
        )

        # act
        created_value = markdown_metadata["created"]
        updated_value = markdown_metadata["updated"]

        # assert
        self.assertEqual(isinstance(created_value, datetime), True)
        self.assertEqual(isinstance(updated_value, datetime), True)

    def test__setitem__given_datetime_data(self):
        # arrange
        markdown_metadata = MarkdownMetadata(metadata_dict={})
        before_datetime_added = markdown_metadata.datetime_data_added

        # act
        markdown_metadata["created"] = datetime.now().isoformat(" ", timespec="seconds")
        after_datetime_added = markdown_metadata.datetime_data_added

        # assert
        self.assertEqual(before_datetime_added, False)
        self.assertEqual(after_datetime_added, True)
        self.assertEqual("created" in markdown_metadata, True)

    def test__setitem__given_data_other_than_datetime_data(self):
        # arrange
        markdown_metadata = MarkdownMetadata(metadata_dict={})
        before_item_added = markdown_metadata.datetime_data_added

        # act
        markdown_metadata["test"] = "test"
        after_item_added = markdown_metadata.datetime_data_added

        # assert
        self.assertEqual(before_item_added, False)
        self.assertEqual(after_item_added, False)
        self.assertEqual("created" in markdown_metadata or "updated" in markdown_metadata, False)

    def test__updated_metadata_with_datetime_data_given_datetime_data(self):
        # arrange
        markdown_metadata = MarkdownMetadata(
            {
                "created": "2023-01-01 00:00:00",
                "updated": "2023-01-01 00:00:00"
            }
        )

        # act
        updated, markdown_metadata = markdown_metadata._update_metadata_with_datetime_data()

        # assert
        self.assertEqual(updated, False)

    def test__updated_metadata_with_datetime_data_without_datetime_data(self):
        # arrange
        markdown_metadata = MarkdownMetadata(metadata_dict={})

        # act
        updated, markdown_metadata = markdown_metadata._update_metadata_with_datetime_data()

        # assert
        self.assertEqual(updated, True)
        self.assertEqual("created" in markdown_metadata and "updated" in markdown_metadata, True)
        self.assertEqual(isinstance(markdown_metadata["created"], datetime), True)

    def test_create_metadata_without_datetime_data(self):
        # arrange
        markdown_metadata = MarkdownMetadata.create_metadata(metadata_dict={})
        
        # act
        is_created_and_updated = "created" in markdown_metadata and "updated" in markdown_metadata
        is_created_isinstance_of_datetime = isinstance(markdown_metadata["created"], datetime)

        # assert
        self.assertEqual(is_created_and_updated, True)
        self.assertEqual(is_created_isinstance_of_datetime, True)
        self.assertEqual(markdown_metadata.datetime_data_added, True)

    def test_create_metadata_with_valid_datetime_data(self):
        # arrange
        markdown_metadata = MarkdownMetadata.create_metadata(
            {
                "created": "2023-01-01 00:00:00",
                "updated": "2023-01-02 00:00:00"
            }
        )

        # act
        is_created_isinstance_of_datetime = isinstance(markdown_metadata["created"], datetime)

        # assert
        self.assertEqual(is_created_isinstance_of_datetime, True)
        self.assertEqual(markdown_metadata.datetime_data_added, False)


    def test_create_metadata_with_invalid_datetime_data(self):
        # arrange
        metadata_dict_with_invalid_datetime_format = {
            "created": "2023-01-01 00:00:0",
            "updated": "2023-01-02 00:00:000"
        }

        # act
        with self.assertRaises(DatetimeDataFormatIsIncorrect) as cm:
            MarkdownMetadata.create_metadata(
                metadata_dict=metadata_dict_with_invalid_datetime_format
            )

        # assert
        self.assertEqual(isinstance(cm.exception, DatetimeDataFormatIsIncorrect), True)

    def test__validate_datetime_format_given_too_short(self):
        # arrange
        too_short_datetime_format = "2023-01-01 00:00:0"

        # act
        retruned_format = _validate_datetime_format(too_short_datetime_format)

        # assert
        self.assertEqual(retruned_format, None)

    def test__validate_datetime_format_given_too_long(self):
        # arrange
        too_long_datetime_format = "2023-01-01 00:00:000"

        # act
        retruned_format = _validate_datetime_format(too_long_datetime_format)

        # assert
        self.assertEqual(retruned_format, None)

    def test__validate_datetime_format_given_valid_format(self):
        # arrange
        valid_datetime_format = "2023-01-01 00:00:00"
        
        # act
        returned_format = _validate_datetime_format(valid_datetime_format)

        # assert
        self.assertEqual(returned_format[0], "2023-01-01 00:00:00")


