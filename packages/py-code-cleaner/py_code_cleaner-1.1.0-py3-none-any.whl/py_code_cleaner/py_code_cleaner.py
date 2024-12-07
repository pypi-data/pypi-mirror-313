
from typing import Optional, Set, Union, Any, Iterable
from typing_extensions import TypeAlias

import os
from pathlib import Path
import shutil
import tempfile

import ast
from ast import Constant
import astunparse  # pip install astunparse


#region UTILS

PathLike: TypeAlias = Union[str, os.PathLike]


def mkdir_of_file(file_path: PathLike):
    """
    creates parent directory of the file
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def read_text(path: PathLike, encoding: str = 'utf-8') -> str:
    return Path(path).read_text(encoding=encoding, errors='ignore')


def write_text(result_path: PathLike, text: str, encoding: str = 'utf-8'):
    mkdir_of_file(result_path)
    Path(result_path).write_text(text, encoding=encoding, errors='ignore')


#endregion


_DOCSTRING_START: str = "'" + '"'
"""chars the docstring can start after unparse"""


class NewLineProcessor(ast.NodeTransformer):
    """class for keeping '\n' chars inside python strings during ast unparse"""
    def visit_Constant(self, node: Constant) -> Any:
        if isinstance(node.value, str):
            node.value = node.value.replace('\n', '\\n')
        return node


class TypeHintRemover(ast.NodeTransformer):
    """ast tree transformer which removes all annotations functional from the code"""

    def visit_FunctionDef(self, node):
        # remove the return type definition
        node.returns = None
        # remove all argument annotations
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        if node.value is None:
            return None
        return ast.Assign([node.target], node.value)

    def visit_Import(self, node):
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node):
        return node if node.module != 'typing' else None


def clean_py(
    file_from: PathLike,
    file_to: PathLike,
    filter_empty_lines: bool = True,
    filter_docstrings: bool = True,
    filter_annotations: bool = True
) -> None:
    """
    remove comments and other data from python files

    Args:
        file_from:
        file_to:
        filter_empty_lines: remove empty lines too
        filter_docstrings: remove docstrings too
        filter_annotations: remove annotations too

    """

    p = Path(file_from)

    assert p.exists(), p
    assert p.suffix == '.py', file_from

    with open(file_from, encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
        except Exception:
            print(f"Error on file {file_from}")
            raise

    if filter_annotations:
        tree = TypeHintRemover().visit(tree)

    tree = NewLineProcessor().visit(tree)

    lines = astunparse.unparse(tree).split('\n')

    if filter_empty_lines:
        lines = (l for l in lines if l)

    if filter_docstrings:
        lines = (l for l in lines if l.lstrip()[:1] not in _DOCSTRING_START)

    write_text(file_to, '\n'.join(lines))


def clean_py_deep(
    dir_from: PathLike,
    dir_to: PathLike,
    keep_nonpy: Optional[Iterable[str]] = ('.pyx', ),
    verbose: bool = True,
    dry_run: bool = False,
    **clean_py_kwargs
) -> None:
    """
    Performs recursive clean_py with directories structure keeping

    Args:
        dir_from:
        dir_to:
        keep_nonpy: non-python extensions for files which must be just copied, other files will be skipped
        verbose: whether to show process stats
        dry_run: whether to not perform any file creation operations
        **clean_py_kwargs:

    """

    inpath = Path(dir_from)
    outpath = Path(dir_to)
    keep_nonpy: Set[str] = set() if keep_nonpy is None else set(keep_nonpy)

    assert inpath.exists(), inpath

    _skipped = _copied = _processed = 0

    for p in inpath.rglob('*'):
        if p.is_dir():
            continue

        t = outpath / p.relative_to(inpath)
        suff = t.suffix

        if suff != '.py':
            if suff in keep_nonpy:
                if not dry_run:
                    mkdir_of_file(t)
                    shutil.copyfile(p, t)
                _copied += 1
            else:
                _skipped += 1
        else:
            if not dry_run:
                clean_py(p, t, **clean_py_kwargs)
            _processed += 1

    if verbose:
        print(
            f"Total files:         {_skipped + _copied + _processed}\n"
            f" skipped non-python: {_skipped}\n"
            f"  copied non-python: {_copied}\n"
            f"   processed python: {_processed}"
        )


def clean_py_main(
    src: PathLike,
    dst: Optional[PathLike] = None,
    keep_nonpy: Optional[Iterable[str]] = ('.pyx',),
    filter_empty_lines: bool = True,
    filter_docstrings: bool = True,
    filter_annotations: bool = True,
    quiet: bool = False,
    dry_run: bool = False
):
    """
    perform cleaning process from src to dst
    Args:
        src: python file path or path to directory with files
        dst: destination file or directory; empty means to print to stdout
        keep_nonpy: additional file extensions to transfer between src and dst directories (to not ignore)
        filter_empty_lines: whether to remove empty lines
        filter_docstrings: whether to remove docstrings
        filter_annotations: whether to remove annotations
        quiet: do not process output
        dry_run: do not perform any file creation operations

    Returns:

    """
    assert not quiet * dry_run, (quiet, dry_run, '--quiet and --dry-run cannot be true both')
    verbose = not quiet

    src = Path(src)
    assert src.exists(), src
    if src.is_file():
        assert src.suffix == '.py', src

    filter_kwargs = dict(
        filter_empty_lines=filter_empty_lines,
        filter_docstrings=filter_docstrings,
        filter_annotations=filter_annotations
    )

    if dst:  # destination provided
        dst = Path(dst)

        if src.is_file():
            if dst.exists() and dst.is_dir():  # file into folder
                dst = dst.parent / src.name

            if verbose:
                print(f"Clean {str(src)} -> {str(dst)}")
            if not dry_run:
                clean_py(src, dst, **filter_kwargs)
        else:
            if dst.exists():
                assert dst.is_dir(), f"src {str(src)} if dir, but dst {str(dst)} is not"

            if verbose:
                print(f"Clean directory {str(src)} -> {str(dst)}")
            clean_py_deep(
                src, dst,
                keep_nonpy=keep_nonpy,
                verbose=verbose,
                dry_run=dry_run,
                **filter_kwargs
            )

    else:  # no destination

        assert not dry_run, '--dry-run for no destination is not supported'
        assert src.is_file(), 'source as directory for no destination is not supported'

        import time
        dst = os.path.join(tempfile.gettempdir(), f'clean-py-no-dst{time.time()}')
        clean_py(src, dst, **filter_kwargs)
        print(read_text(dst))
        os.unlink(dst)


def clean_py_many(
    src: Iterable[PathLike],
    dst: PathLike,
    keep_nonpy: Optional[Iterable[str]] = ('.pyx',),
    filter_empty_lines: bool = True,
    filter_docstrings: bool = True,
    filter_annotations: bool = True,
    quiet: bool = False,
    dry_run: bool = False
):
    """
    performs clean-py operation for many sources
    Args:
        src: sequence of files or folders
        dst: destination folder to save results
        keep_nonpy:
        filter_empty_lines:
        filter_docstrings:
        filter_annotations:
        quiet:
        dry_run:

    Notes:
        absolute paths will be cut to their base names, it is recommended to use relative paths
    """

    assert not isinstance(src, str), f'only string sequence! {src}'

    src = list(src)
    assert src, 'no inputs'

    dst = Path(dst)
    if dst.exists():
        assert dst.is_dir(), f"target destination {dst} exists and is not a directory"

    for s in src:
        s = Path(s)
        clean_py_main(
            src=s,
            dst=dst / (
                s.name if s.is_absolute() else '/'.join(p for p in s.parts if p != '..')
            ),
            keep_nonpy=keep_nonpy, filter_docstrings=filter_docstrings, filter_annotations=filter_annotations,
            filter_empty_lines=filter_empty_lines, quiet=quiet, dry_run=dry_run
        )

