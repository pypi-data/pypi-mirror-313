
# Schemantis CLI

## Introduction

The Schemantis CLI is a command-line interface tool that allows you to generate code from map data using the Schemantis API.

## Installation

To install the Schemantis CLI, you can use pip:

```bash
pip install schemantis-cli
```

## Usage

To use the Schemantis CLI, you need to provide the following arguments:

- `--generator` or `-g`: The generator to use (e.g., 'python').
- `--map_id_or_name` or `-m`: The map ID or name.
- `--output-directory` or `-o`: The output directory for the generated code.

Here is an example command to generate Python code from a map:

```bash
schemantis-cli --generator python --map_id_or_name 123 --output-directory ./out
```
