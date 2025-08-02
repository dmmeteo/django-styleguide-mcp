#!/usr/bin/env python3
"""Command-line interface for mcpdoc-split."""

import argparse
import sys
from pathlib import Path

from mcpdoc_split._version import __version__
from mcpdoc_split.main import generate_docs
from mcpdoc_split.splash import SPLASH


EPILOG = """
Examples:
  # Basic usage - split README.md into docs/ directory
  mcpdoc-split README.md

  # Specify custom output directory and TOC file
  mcpdoc-split README.md --output-dir documentation --toc-file toc.md

  # Generate with custom URL structure  
  mcpdoc-split README.md \\
    --url-prefix https://mysite.com \\
    --base-path /guide \\
    --max-level 6 \\
    --toc-file docs/table-of-contents.md

  # Split only top-level headers (H1 and H2)
  mcpdoc-split README.md --max-level 3

  # Show version with ASCII art splash screen
  mcpdoc-split --version

  # Show ASCII art splash screen
  mcpdoc-split --splash
"""


class CustomFormatter(
    argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    """Custom formatter to preserve epilog formatting while showing default values."""

    pass


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Split large markdown files into smaller documents with TOC generation",
        formatter_class=CustomFormatter,
        epilog=EPILOG,
    )

    # Main input argument
    parser.add_argument("input_file", nargs="?", help="Path to the markdown file to split")

    # Output options
    parser.add_argument(
        "--output-dir", "-o", default="docs", help="Output directory for split files"
    )
    
    parser.add_argument(
        "--toc-file", "-t", default="llms.txt", help="Path to the TOC file to generate"
    )

    # URL generation options
    parser.add_argument(
        "--url-prefix",
        "-u",
        default="https://example.com",
        help="URL prefix for absolute links in TOC",
    )

    parser.add_argument(
        "--base-path", "-b", default="/docs", help="Base path for docs in URLs"
    )

    # Content options
    parser.add_argument(
        "--max-level",
        "-m",
        type=int,
        default=6,
        choices=range(1, 7),
        metavar="1-6",
        help="Maximum header level to split at (1=H1, 2=H2, etc.)",
    )

    # Version information
    parser.add_argument(
        "--version",
        "-V",
        action="store_true",
        help="Show version information and exit",
    )

    # Splash screen
    parser.add_argument(
        "--splash",
        action="store_true",
        help="Show ASCII art splash screen and exit",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI."""
    # Check if any arguments were provided
    if len(sys.argv) == 1:
        # No arguments, print help
        help_parser = argparse.ArgumentParser(
            description="Split large markdown files into smaller documents with TOC generation",
            formatter_class=CustomFormatter,
            epilog=EPILOG,
        )
        # Add version to help parser too
        help_parser.add_argument(
            "--version",
            "-V",
            action="store_true",
            help="Show version information and exit",
        )
        help_parser.add_argument(
            "--splash",
            action="store_true",
            help="Show ASCII art splash screen and exit",
        )
        help_parser.print_help()
        sys.exit(0)

    args = parse_args()

    # Handle version
    if args.version:
        print(SPLASH)
        print(f"mcpdoc-split {__version__}")
        print("Split large markdown files into smaller documents with TOC generation")
        print()
        sys.exit(0)

    # Handle splash screen
    if args.splash:
        print(SPLASH)
        print(f"mcpdoc-split {__version__}")
        print("Split large markdown files into smaller documents with TOC generation")
        print()
        sys.exit(0)

    # Check if input_file is required
    if not args.input_file:
        print("Error: input_file is required when not using --version or --splash", file=sys.stderr)
        sys.exit(1)

    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print(f"Error: '{args.input_file}' is not a file", file=sys.stderr)
        sys.exit(1)

    # Check if input file has .md extension (warning, not error)
    if not input_path.suffix.lower() in [".md", ".markdown"]:
        print(f"Warning: '{args.input_file}' doesn't appear to be a markdown file")

    try:
        # Call the main function
        generate_docs(
            input_file=args.input_file,
            output_dir=args.output_dir,
            url_prefix=args.url_prefix,
            base_path=args.base_path,
            max_level=args.max_level,
            toc_file=args.toc_file,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
