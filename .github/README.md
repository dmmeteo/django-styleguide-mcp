# GitHub Automation

This directory contains automated workflows for the mcpdoc-split project:

## Dependabot Configuration

- **dependabot.yml** - Automatically updates the django-styleguide submodule weekly

## Workflows

- **submodule-docs-update.yml** - Regenerates documentation when submodule updates
- **auto-merge-dependabot.yml** - Automatically merges approved Dependabot PRs
- **run-tests.yml** - Runs unit tests on pull requests and pushes

## Automation Flow

1. Dependabot creates PR with submodule update
2. Tests run automatically
3. Documentation regenerates automatically
4. If all checks pass, PR is auto-merged
5. Updated docs are available in the main branch

This provides fully automated maintenance of the django-styleguide documentation.
