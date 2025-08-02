"""Tests for mcpdoc_split.cli module."""

import sys
from unittest.mock import patch, MagicMock
from io import StringIO

from mcpdoc_split.cli import parse_args, main


class TestParseArgs:
    """Test command line argument parsing."""

    def test_minimal_args(self):
        """Test parsing minimal required arguments."""
        with patch.object(sys, "argv", ["mcpdoc-split", "test.md"]):
            args = parse_args()
            assert args.input_file == "test.md"
            assert args.output_dir == "docs"
            assert args.url_prefix == "https://example.com"
            assert args.base_path == "/docs"
            assert args.max_level == 6

    def test_all_args(self):
        """Test parsing all arguments."""
        with patch.object(
            sys,
            "argv",
            [
                "mcpdoc-split",
                "input.md",
                "--output-dir",
                "output",
                "--url-prefix",
                "https://test.com",
                "--base-path",
                "/guide",
                "--max-level",
                "2",
            ],
        ):
            args = parse_args()
            assert args.input_file == "input.md"
            assert args.output_dir == "output"
            assert args.url_prefix == "https://test.com"
            assert args.base_path == "/guide"
            assert args.max_level == 2

    def test_short_args(self):
        """Test parsing short arguments."""
        with patch.object(
            sys,
            "argv",
            [
                "mcpdoc-split",
                "input.md",
                "-o",
                "output",
                "-u",
                "https://test.com",
                "-b",
                "/guide",
                "-m",
                "2",
            ],
        ):
            args = parse_args()
            assert args.input_file == "input.md"
            assert args.output_dir == "output"
            assert args.url_prefix == "https://test.com"
            assert args.base_path == "/guide"
            assert args.max_level == 2


class TestMain:
    """Test main function."""

    @patch("mcpdoc_split.cli.generate_docs")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_file")
    def test_successful_execution(self, mock_is_file, mock_exists, mock_generate_docs):
        """Test successful execution of main function."""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        with patch.object(sys, "argv", ["mcpdoc-split", "test.md"]):
            try:
                main()
            except SystemExit:
                pass  # main() calls sys.exit(0) on success

            mock_generate_docs.assert_called_once()

    @patch("builtins.print")
    @patch("pathlib.Path.exists")
    def test_file_not_found(self, mock_exists, mock_print):
        """Test handling of non-existent input file."""
        mock_exists.return_value = False

        with patch.object(sys, "argv", ["mcpdoc-split", "nonexistent.md"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 1

            # Check that error message was printed
            mock_print.assert_called()
            args, kwargs = mock_print.call_args
            assert "not found" in args[0]

    @patch("builtins.print")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_file")
    def test_not_a_file(self, mock_is_file, mock_exists, mock_print):
        """Test handling when input is not a file."""
        mock_exists.return_value = True
        mock_is_file.return_value = False

        with patch.object(sys, "argv", ["mcpdoc-split", "directory"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 1

            # Check that error message was printed
            mock_print.assert_called()
            args, kwargs = mock_print.call_args
            assert "not a file" in args[0]

    def test_no_args_shows_help(self):
        """Test that no arguments shows help."""
        with patch.object(sys, "argv", ["mcpdoc-split"]):
            with patch.object(sys, "stdout", new=StringIO()):
                try:
                    main()
                except SystemExit as e:
                    assert e.code == 0
