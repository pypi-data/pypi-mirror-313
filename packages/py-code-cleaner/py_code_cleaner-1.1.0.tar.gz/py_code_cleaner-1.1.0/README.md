[![PyPI version](https://badge.fury.io/py/py-code-cleaner.svg)](https://pypi.org/project/py-code-cleaner/)
[![Downloads](https://pepy.tech/badge/py-code-cleaner)](https://pepy.tech/project/py-code-cleaner)
[![Downloads](https://pepy.tech/badge/py-code-cleaner/month)](https://pepy.tech/project/py-code-cleaner)
[![Downloads](https://pepy.tech/badge/py-code-cleaner/week)](https://pepy.tech/project/py-code-cleaner)


# py-code-cleaner

Small PyPI package provides python code cleaning from comments, docstrings, annotations. Primary I use it for automated checks whether no code in the python files has been changed whatever new lines or comments added.

```
pip install py-code-cleaner
```

```py
from py-code-cleaner import clean_py, clean_py_deep, clean_py_main

# def clean_py_main(
#     src: PathLike,
#     dst: Optional[PathLike] = None,
#     keep_nonpy: Optional[Iterable[str]] = ('.pyx',),
#     filter_empty_lines: bool = True,
#     filter_docstrings: bool = True,
#     filter_annotations: bool = True,
#     quiet: bool = False,
#     dry_run: bool = False
# )
```

## CLI 

```sh
clean-py -h
```

```
usage: clean-py [-h] [--destination DESTINATION] [--keep-nonpy KEEP_NONPY [KEEP_NONPY ...]] [--keep-empty-lines] [--keep-docstrings] [--keep-annotations] [--quiet] [--dry-run] source

Cleanses *.py files from comments, empty lines, annotations and docstrings

positional arguments:
  source                python file path or path to directory with files

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION, -d DESTINATION
                        destination file or directory; empty means to print to stdout (default: None)
  --keep-nonpy KEEP_NONPY [KEEP_NONPY ...], -k KEEP_NONPY [KEEP_NONPY ...]
                        additional file extensions to transfer between src and dst directories (to not ignore) (default: )
  --keep-empty-lines, -e
                        Whether to not remove empty lines (default: False)
  --keep-docstrings, -s
                        Whether to not remove docstrings (default: False)
  --keep-annotations, -a
                        Whether to not remove annotations (default: False)
  --quiet, -q           Do not print processing info (default: False)
  --dry-run, -n         Whether to run without performing file processing operations (default: False)
```
