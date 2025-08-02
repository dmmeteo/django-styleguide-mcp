"""Tests for mcpdoc_split.cli module."""

import sys
from unittest.mock import patch, MagicMock
from io import StringIO
import pytest

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
            assert args.toc_file == "llms.txt"

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
                "--toc-file",
                "custom_toc.md",
            ],
        ):
            args = parse_args()
            assert args.input_file == "input.md"
            assert args.output_dir == "output"
            assert args.url_prefix == "https://test.com"
            assert args.base_path == "/guide"
            assert args.max_level == 2
            assert args.toc_file == "custom_toc.md"

    def test_short_args(self):
        """Test parsing short arguments."""
        with patch.object(
            sys,
            "argv",
            [
                "mcpdoc-split",
                "input.md",
                "-o",
                "out",
                "-u",
                "https://example.org",
                "-b",
                "/docs",
                "-m",
                "3",
                "-t",
                "toc.md",
            ],
        ):
            args = parse_args()
            assert args.input_file == "input.md"
            assert args.output_dir == "out"
            assert args.url_prefix == "https://example.org"
            assert args.base_path == "/docs"
            assert args.max_level == 3
            assert args.toc_file == "toc.md"

    def test_version_arg(self):
        """Test parsing --version argument."""
        with patch.object(sys, "argv", ["mcpdoc-split", "--version"]):
            args = parse_args()
            assert args.version is True
            assert args.input_file is None

    def test_splash_arg(self):
        """Test parsing --splash argument."""
        with patch.object(sys, "argv", ["mcpdoc-split", "--splash"]):
            args = parse_args()
            assert args.splash is True
            assert args.input_file is None


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

    def test_version_shows_splash(self):
        """Test that --version shows splash screen and version."""
        with patch.object(sys, "argv", ["mcpdoc-split", "--version"]):
            with patch.object(sys, "stdout", new=StringIO()) as mock_stdout:
                try:
                    main()
                except SystemExit as e:
                    assert e.code == 0

                output = mock_stdout.getvalue()
                assert "███" in output  # Check for ASCII art
                assert "mcpdoc-split" in output
                assert "0.2.1" in output

    def test_splash_shows_splash(self):
        """Test that --splash shows splash screen."""
        with patch.object(sys, "argv", ["mcpdoc-split", "--splash"]):
            with patch.object(sys, "stdout", new=StringIO()) as mock_stdout:
                try:
                    main()
                except SystemExit as e:
                    assert e.code == 0
                
                output = mock_stdout.getvalue()
                assert "███" in output  # Check for ASCII art
                assert "mcpdoc-split" in output
                assert "Split large markdown files" in output

    def test_missing_input_file_error(self):
        """Test that missing input file when not using special flags shows error."""
        with patch.object(sys, "argv", ["mcpdoc-split", "--output-dir", "test"]):
            with patch.object(sys, "stderr", new=StringIO()) as mock_stderr:
                try:
                    main()
                except SystemExit as e:
                    assert e.code == 1
                
                error_output = mock_stderr.getvalue()
                assert "input_file is required" in error_output
