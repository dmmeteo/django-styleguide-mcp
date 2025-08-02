# Django Styleguide for MCP Servers

Ready-to-use Django Styleguide documentation for Model Context Protocol (MCP) servers in Cursor, Windsurf, Claude Desktop, and other AI editors.

## What is this?

This repository takes the original [Django Styleguide](https://github.com/dmmeteo/Django-Styleguide) documentation as a git submodule, automatically splits it into smaller, AI-friendly files and provides access to them through the [llms.txt](https://llmstxt.org/) format.

**Result:** Your AI assistant can easily find and use all Django best practices from the original styleguide.

## How it works

1. **Git submodule**: We include the original Django Styleguide as a submodule
2. **AST-based splitting**: CLI tool uses markdown-it-py to parse and split the large README.md into separate files by sections  
3. **Configurable TOC generation**: Creates an index file (llms.txt by default) with absolute URLs for each section
4. **Ready for consumption**: MCP servers can easily access the documentation

## What you get

- 📄 **20+ separate files** with Django best practices (Models, Services, APIs, etc.)
- 🔗 **Configurable TOC file** with direct links to GitHub raw content
- ⚡ **AST-based parsing** for reliable and fast processing
- 🔄 **Automatic updates** when the original styleguide changes
- 🤖 **AI-friendly format** for MCP servers

## Automation Features

This repository includes full automation through GitHub Actions and Dependabot:

- 🔄 **Weekly automatic submodule updates** via Dependabot
- 📚 **Automatic documentation regeneration** when submodule changes  
- ✅ **Automatic testing** on every update
- 🚀 **Auto-merge** for successful updates (tests pass + docs updated)
- 🎨 **CLI splash screen** for enhanced user experience

All updates happen automatically - you get fresh Django Styleguide documentation without any manual work.

## Example generated documentation

After processing you get this structure:

```text
docs/
├── models.md                    # Django models
├── services.md                  # Service layer  
├── apis-serializers.md          # APIs and serializers
├── urls.md                      # URL structure
├── settings.md                  # Django settings
├── errors-exception-handling.md # Error handling
├── testing.md                   # Testing
├── celery.md                    # Celery tasks
└── ...other sections

llms.txt  # Index for MCP servers
```

**llms.txt** contains direct links:

```markdown
# Table of Contents

- [Models](https://raw.githubusercontent.com/dmmeteo/django-styleguide-mcp/main/docs/models.md)
- [Services](https://raw.githubusercontent.com/dmmeteo/django-styleguide-mcp/main/docs/services.md)
- [APIs & Serializers](https://raw.githubusercontent.com/dmmeteo/django-styleguide-mcp/main/docs/apis-serializers.md)
...
```

## Integration with AI editors

### Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "django-styleguide": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "DjangoStyleguide:https://raw.githubusercontent.com/dmmeteo/django-styleguide-mcp/main/llms.txt",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

Add to your Cursor Rules:

```text
For ANY questions about Django best practices, use the django-styleguide MCP server:
+ call list_doc_sources to get available sources
+ call fetch_docs to read llms.txt
+ analyze URLs in llms.txt based on the question  
+ fetch relevant documentation sections
+ provide comprehensive answers based on Django Styleguide
```

### Windsurf

Similar configuration in `~/.codeium/windsurf/mcp_config.json`.

### Claude Desktop

Add to `~/Library/Application\ Support/Claude/claude_desktop_config.json`.

## Keeping documentation up-to-date

Documentation automatically updates when the original Django Styleguide changes:

```bash
# 1. Git submodule automatically updates
git submodule update --remote django-styleguide

# 2. Regenerate documentation with new CLI options
uv run python -m mcpdoc_split.cli django-styleguide/README.md \
    --url-prefix "https://raw.githubusercontent.com/dmmeteo/django-styleguide-mcp/main" \
    --base-path "/docs" \
    --max-level 2 \
    --toc-file llms.txt

# 3. Commit changes
git add docs/ llms.txt
git commit -m "Update documentation from Django Styleguide"
```

## Development

If you want to make changes or run locally:

```bash
# Clone repository
git clone https://github.com/dmmeteo/django-styleguide-mcp.git
cd django-styleguide-mcp

# Initialize submodule
git submodule update --init --recursive

# Install dependencies
uv sync

# Run CLI
uv run python -m mcpdoc_split.cli django-styleguide/README.md

# Run tests  
uv run pytest
```

## CLI Usage

The `mcpdoc-split` CLI tool offers flexible options for customizing the documentation generation:

```bash
# Basic usage
uv run python -m mcpdoc_split.cli django-styleguide/README.md

# Custom output directory and TOC file
uv run python -m mcpdoc_split.cli django-styleguide/README.md \
    --output-dir documentation \
    --toc-file table-of-contents.md

# Full customization with URL structure
uv run python -m mcpdoc_split.cli django-styleguide/README.md \
    --url-prefix "https://mysite.com" \
    --base-path "/guide" \
    --max-level 3 \
    --toc-file docs/index.md

# Only split top-level sections (H1 and H2)
uv run python -m mcpdoc_split.cli django-styleguide/README.md --max-level 2
```

## Project structure

```text
mcpdoc_split/           # CLI tool for splitting documentation
├── cli.py              # Command line interface with configurable options
├── main.py             # AST-based file splitting logic using markdown-it-py
└── ...

django-styleguide/      # Git submodule of original styleguide
docs/                   # Generated documentation files  
llms.txt               # Configurable index file for MCP servers
tests/                 # Comprehensive test suite
```

## Acknowledgments

- [Django Styleguide](https://github.com/dmmeteo/Django-Styleguide) by HackSoft for excellent Django practices
- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) for reliable markdown parsing with AST support
- [mcpdoc](https://github.com/langchain-ai/mcpdoc) by LangChain for MCP server inspiration
- [Model Context Protocol](https://github.com/modelcontextprotocol) for the MCP specification

## Technical Details

This tool uses a **single-pass AST algorithm** for optimal performance:

1. **markdown-it-py** parses the markdown into an Abstract Syntax Tree (AST)
2. **One-pass processing** simultaneously generates TOC and section files
3. **Line-based content extraction** ensures perfect formatting preservation
4. **Configurable output** supports custom TOC file paths and URL structures

## Related projects

- [Django Styleguide](https://github.com/dmmeteo/Django-Styleguide) - The original Django best practices guide
- [mcpdoc](https://github.com/langchain-ai/mcpdoc) - MCP server for documentation access
- [llms.txt](https://llmstxt.org/) - Standard for AI-friendly documentation
