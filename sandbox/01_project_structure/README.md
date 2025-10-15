# Experiments & Setup Documentation

This directory contains experimental code and detailed setup documentation that was created during the project restructuring.

## Setup Documentation

These documents detail how the project was restructured and organized:

### [CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)

Details about how the root directory was cleaned up and files were organized into proper directories.

### [FINAL_STRUCTURE.md](FINAL_STRUCTURE.md)

Final project structure after organizing the `config/` directory for keywords and configuration files.

### [PRE_COMMIT_SETUP.md](PRE_COMMIT_SETUP.md)

Complete guide on pre-commit hooks that were added to the project for automatic code quality checks.

### [STRUCTURE_OVERVIEW.md](STRUCTURE_OVERVIEW.md)

Overview of the complete project structure showing all directories and their purposes.

## Purpose

This documentation provides:

- **Historical record** of project organization decisions
- **Examples** of professional project structure
- **Reference** for similar restructuring projects
- **Learning resource** for understanding the architecture

## For Current Documentation

For up-to-date documentation, see:

- **[README.md](../../README.md)** - Main project documentation
- **[docs/](../../docs/)** - All current documentation
  - Quick Start Guide
  - Contributing Guidelines
  - Release Policy
  - Project Structure
  - Pre-commit Guide

## Experiments

Use this directory for:

- Testing new features
- Trying different approaches
- Prototyping code
- Temporary experiments

Keep experimental code isolated from the main codebase until it's ready for production.

## Example Experiment Structure

```text
sandbox/experiments/
├── README.md                    # This file
├── CLEANUP_SUMMARY.md           # Setup docs
├── FINAL_STRUCTURE.md           # Setup docs
├── PRE_COMMIT_SETUP.md          # Setup docs
├── STRUCTURE_OVERVIEW.md        # Setup docs
├── experiment_async_search.py   # Example experiment
└── experiment_new_parser.py     # Example experiment
```

## Running Experiments

```bash
# From project root
cd sandbox/experiments

# Run your experiment
python experiment_async_search.py
```

## Best Practices

1. **Name clearly** - Use descriptive names like `experiment_feature_name.py`
2. **Document** - Add comments explaining what you're testing
3. **Isolate** - Don't import from main package unless testing integration
4. **Clean up** - Remove or archive experiments when done
5. **Reference** - If experiment succeeds, reference it when implementing in main code

---

## Keep experimenting
