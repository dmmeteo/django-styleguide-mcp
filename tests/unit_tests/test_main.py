"""Tests for mcpdoc_split.main module."""

import pytest
import tempfile
import os
from pathlib import Path

from mcpdoc_split.main import (
    generate_filename,
    generate_anchor_link,
    extract_headers_from_toc,
    transform_toc_links,
    generate_docs,
)


class TestGenerateFilename:
    """Test the generate_filename function."""

    def test_simple_header(self):
        """Test simple header conversion."""
        assert generate_filename("Introduction") == "introduction.md"

    def test_header_with_spaces(self):
        """Test header with spaces."""
        assert generate_filename("Getting Started") == "getting-started.md"

    def test_header_with_special_chars(self):
        """Test header with special characters."""
        assert generate_filename("API & Configuration") == "api-configuration.md"

    def test_empty_header(self):
        """Test empty header."""
        assert generate_filename("") == "untitled.md"

    def test_header_with_multiple_spaces(self):
        """Test header with multiple spaces."""
        assert generate_filename("Multiple   Spaces") == "multiple-spaces.md"

    def test_header_with_numbers(self):
        """Test header with numbers."""
        assert generate_filename("Chapter 1: Overview") == "chapter-1-overview.md"


class TestGenerateAnchorLink:
    """Test the generate_anchor_link function."""

    def test_simple_header(self):
        """Test simple header anchor."""
        assert generate_anchor_link("Introduction") == "#introduction"

    def test_header_with_spaces(self):
        """Test header with spaces."""
        assert generate_anchor_link("Getting Started") == "#getting-started"

    def test_header_with_special_chars(self):
        """Test header with special characters."""
        assert generate_anchor_link("API & Configuration") == "#api-configuration"

    def test_empty_header(self):
        """Test empty header."""
        assert generate_anchor_link("") == "#"


class TestExtractHeadersFromToc:
    """Test the extract_headers_from_toc function."""

    def test_simple_toc(self):
        """Test extracting headers from simple TOC."""
        toc = """- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)"""

        headers = extract_headers_from_toc(toc)

        assert len(headers) == 4
        assert headers[0] == {
            "title": "Introduction",
            "level": 1,
            "anchor": "#introduction",
        }
        assert headers[1] == {
            "title": "Getting Started",
            "level": 1,
            "anchor": "#getting-started",
        }
        assert headers[2] == {
            "title": "Installation",
            "level": 2,
            "anchor": "#installation",
        }
        assert headers[3] == {"title": "Usage", "level": 2, "anchor": "#usage"}

    def test_empty_toc(self):
        """Test empty TOC."""
        headers = extract_headers_from_toc("")
        assert headers == []

    def test_malformed_toc(self):
        """Test malformed TOC."""
        toc = "This is not a valid TOC"
        headers = extract_headers_from_toc(toc)
        assert headers == []


class TestTransformTocLinks:
    """Test the transform_toc_links function."""

    def test_simple_transformation(self):
        """Test simple link transformation."""
        toc = "- [Introduction](#introduction)\n- [Getting Started](#getting-started)"
        file_mapping = {
            "#introduction": "introduction.md",
            "#getting-started": "getting-started.md",
        }
        url_prefix = "https://example.com"
        base_path = "/docs"

        transformed = transform_toc_links(toc, file_mapping, url_prefix, base_path)

        expected = "- [Introduction](https://example.com/docs/introduction.md)\n- [Getting Started](https://example.com/docs/getting-started.md)"
        assert transformed == expected

    def test_no_matching_anchors(self):
        """Test transformation with no matching anchors."""
        toc = "- [Introduction](#introduction)"
        file_mapping = {}
        url_prefix = "https://example.com"
        base_path = "/docs"

        transformed = transform_toc_links(toc, file_mapping, url_prefix, base_path)

        # Should remain unchanged
        assert transformed == toc


class TestGenerateDocs:
    """Test the generate_docs function."""

    def test_file_not_found(self):
        """Test handling of non-existent file."""
        with pytest.raises(FileNotFoundError):
            generate_docs("non_existent_file.md")

    def test_invalid_max_level(self):
        """Test handling of invalid max_level."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\nContent")
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="max_level must be between 1 and 6"):
                generate_docs(temp_file, max_level=0)

            with pytest.raises(ValueError, match="max_level must be between 1 and 6"):
                generate_docs(temp_file, max_level=7)
        finally:
            os.unlink(temp_file)

    def test_basic_generation(self):
        """Test basic document generation."""
        markdown_content = """# Introduction
This is the introduction.

## Getting Started
This is how to get started.

### Installation
Install instructions here.

## Advanced Usage
Advanced topics.
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            temp_file = f.name

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                generate_docs(
                    input_file=temp_file,
                    output_dir=temp_dir,
                    url_prefix="https://test.com",
                    base_path="/test",
                    max_level=2,
                )

                # Check that files were created
                output_path = Path(temp_dir)
                files = list(output_path.glob("*.md"))

                # Should have at least some files
                assert len(files) >= 2

                # Check that llms.txt was created
                llms_file = Path("llms.txt")
                assert llms_file.exists()

                # Clean up llms.txt
                if llms_file.exists():
                    llms_file.unlink()

            finally:
                os.unlink(temp_file)
