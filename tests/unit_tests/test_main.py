"""Tests for mcpdoc_split.main module."""

import pytest
import tempfile
import os
from pathlib import Path

from mcpdoc_split.main import (
    generate_filename,
    generate_anchor_link,
    extract_heading_text,
    save_section_by_lines,
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


class TestExtractHeadingText:
    """Test the extract_heading_text function."""

    def test_extract_heading_text(self):
        """Test extracting heading text from tokens."""
        # Mock tokens structure
        class MockToken:
            def __init__(self, token_type, content=None):
                self.type = token_type
                self.content = content

        tokens = [
            MockToken("heading_open"),
            MockToken("inline", "Test Header"),
            MockToken("heading_close"),
        ]

        result = extract_heading_text(tokens, 0)
        assert result == "Test Header"

    def test_extract_heading_text_not_found(self):
        """Test when heading text is not found."""
        class MockToken:
            def __init__(self, token_type, content=None):
                self.type = token_type
                self.content = content

        tokens = [
            MockToken("heading_open"),
            MockToken("other_token"),
        ]

        result = extract_heading_text(tokens, 0)
        assert result is None


class TestSaveSectionByLines:
    """Test the save_section_by_lines function."""

    def test_save_section_basic(self):
        """Test basic section saving."""
        content_lines = [
            "# Header",
            "This is content.",
            "More content.",
            "## Next Header"
        ]
        
        section = {
            "filename": "test.md",
            "start_line": 0,
            "end_line": 3
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            save_section_by_lines(section, content_lines, temp_dir)
            
            output_file = Path(temp_dir) / "test.md"
            assert output_file.exists()
            
            with open(output_file, 'r') as f:
                saved_content = f.read()
            
            expected_content = "# Header\nThis is content.\nMore content."
            assert saved_content == expected_content


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
            toc_file = os.path.join(temp_dir, "test_toc.txt")
            
            try:
                generate_docs(
                    input_file=temp_file,
                    output_dir=temp_dir,
                    url_prefix="https://test.com",
                    base_path="/test",
                    max_level=2,
                    toc_file=toc_file,
                )

                # Check that files were created
                output_path = Path(temp_dir)
                files = list(output_path.glob("*.md"))

                # Should have at least some files
                assert len(files) >= 2

                # Check that custom TOC file was created
                assert Path(toc_file).exists()

                # Check TOC content
                with open(toc_file, 'r') as f:
                    toc_content = f.read()
                
                assert "# Table of Contents" in toc_content
                assert "https://test.com/test/" in toc_content

            finally:
                os.unlink(temp_file)

    def test_custom_toc_file_path(self):
        """Test custom TOC file path with subdirectory."""
        markdown_content = """# Test Header
Test content.
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            temp_file = f.name

        with tempfile.TemporaryDirectory() as temp_dir:
            # TOC file in subdirectory
            toc_subdir = os.path.join(temp_dir, "subdir")
            toc_file = os.path.join(toc_subdir, "custom_toc.md")
            
            try:
                generate_docs(
                    input_file=temp_file,
                    output_dir=temp_dir,
                    toc_file=toc_file,
                )

                # Check that TOC file was created in subdirectory
                assert Path(toc_file).exists()
                assert Path(toc_subdir).exists()

            finally:
                os.unlink(temp_file)

    def test_max_level_filtering(self):
        """Test that max_level properly filters headers."""
        markdown_content = """# Level 1
Content 1.

## Level 2
Content 2.

### Level 3
Content 3.

#### Level 4
Content 4.
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(markdown_content)
            temp_file = f.name

        with tempfile.TemporaryDirectory() as temp_dir:
            toc_file = os.path.join(temp_dir, "toc.txt")
            
            try:
                # Test with max_level=2 (should include H1 and H2 only)
                generate_docs(
                    input_file=temp_file,
                    output_dir=temp_dir,
                    max_level=2,
                    toc_file=toc_file,
                )

                # Check TOC content
                with open(toc_file, 'r') as f:
                    toc_content = f.read()
                
                # Should include Level 1 and Level 2, but not Level 3 and Level 4
                assert "Level 1" in toc_content
                assert "Level 2" in toc_content
                assert "Level 3" not in toc_content
                assert "Level 4" not in toc_content

            finally:
                os.unlink(temp_file)
