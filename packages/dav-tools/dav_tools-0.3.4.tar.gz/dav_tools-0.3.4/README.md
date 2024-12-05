# dav_tools
Personal Python library to aid in software development

## Installation
```bash
$ pip install dav-tools
```

## Usage on python programs
`dav-tools` contains a variety of diffent submodules, each with its own set of functionalities.

Importing is done in the form of
```python
from dav_tools import <submodule>
```
since it usually doesn't make sense to import the whole library.

## Usage on non-python programs
Some modules can also be executed in other scripts, using:
```bash
python -m dav_tools.modulename [options]
```

Only basic functionalities are available.
Error management requires the original program to exit if a subcommand exits with an error code.