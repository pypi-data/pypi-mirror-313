# winzy-visual-notify

[![PyPI](https://img.shields.io/pypi/v/winzy-visual-notify.svg)](https://pypi.org/project/winzy-visual-notify/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-visual-notify?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-visual-notify/releases)
[![Tests](https://github.com/sukhbinder/winzy-visual-notify/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-visual-notify/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-visual-notify/blob/main/LICENSE)

Notify using visual artefacts like clippy and other things.

## Installation

First configure to install Winzy [to use Winzy](https://github.com/sukhbinder/winzy).

which means.

```bash
pip install winzy
```

Then install this plugin in the same environment as your Winzy application.
```bash
winzy install winzy-visual-notify
```
## Usage

```bash

usage: winzy tell [-h] [-t [TEXT ...]]
                  [-c {dog,dog2,watermellon,bee,ghost,hen,man,pear,purple,random}]

Notify using visual artefacts like clippy and other things.

optional arguments:
  -h, --help            show this help message and exit
  -t [TEXT ...], --text [TEXT ...]
                        Text to display
  -c {dog,dog2,watermellon,bee,ghost,hen,man,pear,purple,random}, --character {dog,dog2,watermellon,bee,ghost,hen,man,pear,purple,random}
                        Name of Character to display

```

## Demo
![winzy tell ](https://raw.githubusercontent.com/sukhbinder/winzy-visual-notify/refs/heads/main/winzy-visual-notify-demo.gif)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-visual-notify
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
