# QuickMD
## Python Markdown Documentation Generator

## Overview

The Python Markdown Documentation Generator is a utility script that automatically generates Markdown documentation from Python files. It extracts details about functions, classes, methods, type hints, and docstrings, and organizes them into a structured Markdown file. This tool is particularly useful for developers who want to maintain clear and organized documentation for their Python projects without manually writing Markdown files.

## Features

- **Automatic Extraction**: Automatically extracts function signatures, type hints, and docstrings from Python files.
- **Class and Method Support**: Supports documenting classes and their associated methods, grouping them appropriately in the output.
- **Structured Output**: Generates well-organized Markdown files, separating functions and classes into different sections.
- **Customizable**: Easily modify the script to tailor the output to your specific needs.

## Installation

To use the Python Markdown Documentation Generator, simply clone this repository:

```bash
pip install QuickMD
```

## Usage
```
qmd md --path <path to file here>
```
A new directory(s) will be made in QuickMDBuild/<path to file> where your .md file will be
