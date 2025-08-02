"""MCP markdown splitter - Split large markdown files into smaller documents."""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Optional

from markdown_it import MarkdownIt


def generate_docs(
    input_file: str,
    output_dir: str = "docs",
    url_prefix: str = "https://example.com",
    base_path: str = "/docs",
    max_level: int = 6,
    toc_file: str = "llms.txt",
) -> None:
    """
    Split a large markdown file into smaller files and generate TOC with absolute URLs.
    Uses a single-pass algorithm through the AST for maximum efficiency.

    Args:
        input_file: Path to the large markdown file to split
        output_dir: Directory to save the split files (default: "docs")
        url_prefix: URL prefix for absolute links (e.g., "https://example.com")
        base_path: Base path for docs (e.g., "/docs")
        max_level: Maximum header level to split at (1=H1, 2=H2, 3=H3, etc.)
        toc_file: Path to the TOC file to generate (default: "llms.txt")

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If max_level is invalid
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if max_level < 1 or max_level > 6:
        raise ValueError("max_level must be between 1 and 6")

    # Clean up existing docs directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Cleaned up existing directory: {output_dir}")

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Read the input file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError as e:
        raise ValueError(f"Unable to read file {input_file}: {e}")

    # Parse markdown to AST
    md = MarkdownIt("commonmark")
    tokens = md.parse(content)

    # Single-pass algorithm: parse AST and generate files + TOC simultaneously
    sections_generated = 0
    
    # Ensure TOC directory exists
    toc_dir = os.path.dirname(toc_file)
    if toc_dir and not os.path.exists(toc_dir):
        Path(toc_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        with open(toc_file, "w", encoding="utf-8") as toc_file_handle:
            toc_file_handle.write("# Table of Contents\n\n")
            
            current_section = None
            content_lines = content.split('\n')
            section_starts = []  # Store all section start positions
            
            # First pass: collect all section starts
            for i, token in enumerate(tokens):
                if token.type == "heading_open" and int(token.tag[1]) <= max_level:
                    header_text = extract_heading_text(tokens, i)
                    if header_text and hasattr(token, 'map') and token.map:
                        section_starts.append({
                            "line": token.map[0],
                            "header": header_text,
                            "level": int(token.tag[1]),
                            "filename": generate_filename(header_text)
                        })
            
            # Second pass: generate sections and TOC
            for idx, section_info in enumerate(section_starts):
                # Write to TOC
                level = section_info["level"]
                header_text = section_info["header"]
                filename = section_info["filename"]
                url = f"{url_prefix.rstrip('/')}{base_path.rstrip('/')}/{filename}"
                indent = "  " * (level - 1)
                toc_file_handle.write(f"{indent}- [{header_text}]({url})\n")
                
                # Determine section boundaries
                start_line = section_info["line"]
                if idx + 1 < len(section_starts):
                    end_line = section_starts[idx + 1]["line"]
                else:
                    end_line = len(content_lines)
                
                # Save section
                section = {
                    "filename": filename,
                    "header": header_text,
                    "level": level,
                    "start_line": start_line,
                    "end_line": end_line
                }
                save_section_by_lines(section, content_lines, output_dir)
                sections_generated += 1
                
    except Exception as e:
        print(f"Warning: Failed to write TOC file {toc_file}: {e}")

    print(f"Documentation generated successfully!")
    print(f"Files saved to: {output_dir}")
    print(f"TOC saved to: {toc_file}")
    print(f"Generated {sections_generated} files (filtered by max_level={max_level})")


def extract_heading_text(tokens: List, heading_open_idx: int) -> Optional[str]:
    """
    Extract heading text from tokens starting at heading_open token.
    
    Args:
        tokens: List of all tokens
        heading_open_idx: Index of heading_open token
        
    Returns:
        Heading text or None if not found
    """
    # Look for the inline token that contains the heading text
    for i in range(heading_open_idx + 1, min(heading_open_idx + 3, len(tokens))):
        token = tokens[i]
        if token.type == "inline":
            return token.content
    return None


def save_section_by_lines(section: Dict, content_lines: List[str], output_dir: str) -> None:
    """
    Save a section to file using line-based approach for perfect reconstruction.
    
    Args:
        section: Section dictionary with line positions
        content_lines: All lines from the original content
        output_dir: Output directory path
    """
    filepath = os.path.join(output_dir, section["filename"])
    
    try:
        start_line = section["start_line"]
        end_line = section.get("end_line", len(content_lines))
        
        # Extract section content directly from original lines
        section_lines = content_lines[start_line:end_line]
        content = "\n".join(section_lines).strip()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    except Exception as e:
        print(f"Warning: Failed to write file {filepath}: {e}")


def generate_filename(header_text: str) -> str:
    """
    Generate a URL-safe filename from header text.

    This follows similar logic to md_toc's anchor generation but for filenames.

    Args:
        header_text: The header text to convert to filename

    Returns:
        A safe filename with .md extension
    """
    # Convert to lowercase
    filename = header_text.lower()

    # Replace spaces and special characters with hyphens
    filename = re.sub(r"[^\w\s-]", "", filename)
    filename = re.sub(r"[-\s]+", "-", filename)

    # Remove leading/trailing hyphens
    filename = filename.strip("-")

    # Ensure we have something
    if not filename:
        filename = "untitled"

    # Add .md extension
    return f"{filename}.md"


def generate_anchor_link(header_text: str) -> str:
    """
    Generate anchor link from header text using GitHub-style formatting.

    This mimics md_toc's anchor generation logic.

    Args:
        header_text: The header text to convert to anchor

    Returns:
        GitHub-style anchor link starting with #
    """
    # Convert to lowercase
    anchor = header_text.lower()

    # Replace spaces with hyphens
    anchor = re.sub(r"\s+", "-", anchor)

    # Remove special characters except hyphens
    anchor = re.sub(r"[^\w\-]", "", anchor)

    # Remove multiple consecutive hyphens
    anchor = re.sub(r"-+", "-", anchor)

    # Remove leading/trailing hyphens
    anchor = anchor.strip("-")

    return f"#{anchor}"
