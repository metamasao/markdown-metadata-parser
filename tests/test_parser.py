from unittest import TestCase

from markdown_metadata_parser.parser import MarkdownParser
from markdown_metadata_parser.exceptions import MetadataNotFoundError


class TestMarkdownParser(TestCase):

    def test_has_metadata_given_valid_content(self):
        # arrange
        valid_content = "---\ntitle: test title\ntags: tag1,tag2\n---\n# Test Heading1"
        
        # act
        markdown_parser = MarkdownParser(content=valid_content)
        is_metadata = markdown_parser.has_metadata()
        
        # assert
        self.assertEqual(is_metadata, True)

    def test_has_metadata_given_invalid_content(self):
        # arrange
        invalid_content = "--\ntitle: test title\ntags: tag1,tag2\n--\n# Test Heading1"

        # act
        markdown_parser = MarkdownParser(content=invalid_content)
        with self.assertRaises(MetadataNotFoundError) as cm:
            markdown_parser.has_metadata()

        # assert
        self.assertEqual(isinstance(cm.exception, MetadataNotFoundError), True)

    def test_has_metadata_given_no_metadata(self):
        invalid_content_no_metadata = "# Test Heading1"

        # act
        markdown_parser = MarkdownParser(content=invalid_content_no_metadata)
        with self.assertRaises(MetadataNotFoundError) as cm:
            markdown_parser.has_metadata()

        # assert
        self.assertEqual(isinstance(cm.exception, MetadataNotFoundError), True)

    def test_parse(self):
        # arrange
        markdown_content = "---\ntitle: test title\nsummary: test summary\ntags: tag1,tag2\n---\n# Test Heading1"
        expected_metadata_dict = {
            "title": "test title",
            "summary": "test summary",
            "tags": "tag1,tag2"
        }
        markdown_parser = MarkdownParser(content=markdown_content)

        # act
        metadata_dict = markdown_parser.parse()

        # assert
        self.assertEqual(metadata_dict, expected_metadata_dict)

    def test_concatenate_new_metadata_and_content_body(self):
        # arrange
        old_content = "---\ntitle: old title\nsummary: old summary\n---\n# Test Heading1"
        markdown_paser = MarkdownParser(content=old_content)

        new_metadata = {
            "title": "new title",
            "summary": "new summary"
        }
        expected_new_content = "---\ntitle: new title\nsummary: new summary\n---\n# Test Heading1"

        # act
        markdown_paser.parse()
        new_content = markdown_paser.concatenate_new_metadata_and_content_body(new_metadata=new_metadata)

        # assert
        self.assertEqual(new_content, expected_new_content)

