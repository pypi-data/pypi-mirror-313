# send-telegram-cli

[![PyPI](https://img.shields.io/pypi/v/send-telegram-cli.svg)](https://pypi.org/project/send-telegram-cli/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/send-telegram-cli?include_prereleases&label=changelog)](https://github.com/sukhbinder/send-telegram-cli/releases)
[![Tests](https://github.com/sukhbinder/send-telegram-cli/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/send-telegram-cli/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/send-telegram-cli/blob/master/LICENSE)

Send Telegram Messages and Other files 

## Installation

Install this tool using `pip`:
```bash
pip install send-telegram-cli
```
## Usage

For help, run:
```bash
sendtele --help
```
You can also use:
```bash
python -m sendtele --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd send-telegram-cli
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
