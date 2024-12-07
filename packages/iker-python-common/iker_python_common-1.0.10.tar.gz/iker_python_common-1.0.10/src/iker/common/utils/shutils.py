import fnmatch
import os
import shutil
from typing import Protocol

from iker.common.utils import logger
from iker.common.utils.sequtils import last, last_or_none, tail
from iker.common.utils.strutils import is_empty

__all__ = [
    "extension",
    "extensions",
    "stem",
    "expanded_path",
    "path_depth",
    "glob_match",
    "listfile",
    "copy",
    "run",
    "execute",
]


def extension(filename: str) -> str:
    """
    Extracts filename extension of the given filename or path

    :param filename: the specific filename or path
    :return: filename extension
    """
    _, result = os.path.splitext(os.path.basename(filename))
    return result


def stem(filename: str, minimal: bool = False) -> str:
    """
    Extracts filename stem of the given filename or path

    :param filename: the specific filename or path
    :param minimal: True if the minimal (shortest) stem is extracted
    :return: filename stem
    """
    base = os.path.basename(filename)
    if not minimal:
        result, _ = os.path.splitext(base)
        return result
    else:
        maximal_extension = last_or_none(extensions(base))
        if is_empty(maximal_extension):
            return base
        else:
            return base[:-len(maximal_extension)]


def extensions(filename: str) -> list[str]:
    """
    Extracts all filename extensions and compound extensions of the given filename or path

    :param filename: the specific filename or path
    :return: list of all extensions ordered from the shortest to the longest
    """
    base = os.path.basename(filename)
    results = [""]
    while True:
        fn, ext = os.path.splitext(base)
        base = fn
        if is_empty(ext):
            break
        results.append(ext + last(results))
    return tail(results)


def expanded_path(path: str) -> str:
    """
    Returns absolute expanded path whose environment vars and home tilde has been expanded

    :param path: the given path
    :return: the absolute canonical path
    """
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def path_depth(root: str, child: str) -> int:
    """
    Returns the relative path depth from the given child to the root

    :param root: the root path
    :param child: the child path
    :return: relative depth
    """
    root_expanded = expanded_path(root)
    child_expanded = expanded_path(child)
    if not child_expanded.startswith(root_expanded):
        return -1
    return child_expanded[len(root_expanded):].count(os.sep)


def glob_match(names: list[str], include_patterns: list[str] = None, exclude_patterns: list[str] = None) -> list[str]:
    """
    Applies the given inclusive and exclusive glob patterns on the given names and returns the filtered result

    :param names: names to apply the glob patterns
    :param include_patterns: inclusive glob patterns
    :param exclude_patterns: exclusive glob patterns
    :return: filtered names
    """
    ret = set()
    for pat in (include_patterns or []):
        ret.update(fnmatch.filter(names, pat))
    if include_patterns is None or len(include_patterns) == 0:
        ret.update(names)
    for pat in (exclude_patterns or []):
        ret.difference_update(fnmatch.filter(names, pat))
    return list(ret)


class CopyFuncProtocol(Protocol):
    def __call__(self, src: str, dst: str, **kwargs) -> None: ...


def listfile(
    path: str,
    *,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
) -> list[str]:
    """
    Recursively scans the given path and returns list of files whose names satisfy the given name patterns and the
    relative depth of their folders to the given root path is not greater than the specific depth value

    :param path: the root path which is scanned
    :param include_patterns: inclusive glob patterns applied to the filenames
    :param exclude_patterns: exclusive glob patterns applied to the filenames
    :param depth: maximum depth of the subdirectories included in the scan
    :return:
    """
    if os.path.exists(path) and not os.path.isdir(path):
        if len(glob_match([os.path.basename(path)], include_patterns, exclude_patterns)) == 0:
            return []
        return [path]

    ret = []
    for parent, dirs, filenames in os.walk(path):
        if 0 < depth <= path_depth(path, parent):
            continue
        for filename in glob_match(filenames, include_patterns, exclude_patterns):
            ret.append(os.path.join(parent, filename))
    return ret


def copy(
    src: str,
    dst: str,
    *,
    include_patterns: list[str] = None,
    exclude_patterns: list[str] = None,
    depth: int = 0,
    follow_symlinks: bool = False,
    ignore_dangling_symlinks: bool = False,
    dirs_exist_ok: bool = False,
    copy_func: CopyFuncProtocol = shutil.copy2
):
    """
    Recursively copies the given source path to the destination path. Only copies the files whose names satisfy the
    given name patterns and the relative depth of their folders to the given source path is not greater than the
    specific depth value

    :param src: the source path or file
    :param dst: the destination path or file
    :param include_patterns: inclusive glob patterns applied to the filenames
    :param exclude_patterns: exclusive glob patterns applied to the filenames
    :param depth: maximum depth of the subdirectories included in the scan
    :param follow_symlinks: True to create symbolic links for the symbolic links present in the source, otherwise, make
    a physical copy
    :param ignore_dangling_symlinks: True to ignore errors if the file pointed by the symbolic link does not exist
    :param dirs_exist_ok: True to ignore errors if the destination directory and subdirectories exist
    :param copy_func: copy function
    """
    if not os.path.isdir(src):
        if len(glob_match([os.path.basename(src)], include_patterns, exclude_patterns)) == 0:
            return
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
        copy_func(src, dst, follow_symlinks=follow_symlinks)
        return

    def ignore_func(parent, names):
        filenames = list(filter(lambda x: not os.path.isdir(os.path.join(parent, x)), names))
        ret = set(filenames)
        if 0 < depth <= path_depth(src, parent):
            return ret
        ret.difference_update(glob_match(filenames, include_patterns, exclude_patterns))
        return ret

    shutil.copytree(src,
                    dst,
                    symlinks=follow_symlinks,
                    ignore=ignore_func,
                    ignore_dangling_symlinks=ignore_dangling_symlinks,
                    dirs_exist_ok=dirs_exist_ok,
                    copy_function=copy_func)


def run(cmd: str) -> bool:
    """
    Runs given command and returns the success status

    :param cmd: command to run

    :return: True if the command has been successfully run
    """
    logger.debug("Running command: %s", cmd)
    return os.system(cmd) == 0


def execute(cmd: str, strip: bool = True) -> str:
    """
    Executes given command and returns contents collected from standard output

    :param cmd: command to execute
    :param strip: True if the contents will be stripped

    :return: the content from standard output
    """
    logger.debug("Executing command: %s", cmd)
    if strip:
        return os.popen(cmd).read().strip()
    return os.popen(cmd).read()
