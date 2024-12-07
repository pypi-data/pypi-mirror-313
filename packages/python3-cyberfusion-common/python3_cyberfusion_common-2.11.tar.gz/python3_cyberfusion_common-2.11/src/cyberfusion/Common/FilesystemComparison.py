"""Helper for comparing filesystem objects."""

import filecmp
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _get_recursive_dircmps(dircmp: filecmp.dircmp) -> List[filecmp.dircmp]:
    """Get dircmp object for every subdirectory.

    Subdirectories are only returned for directories that are in the left and
    right directories.
    """
    dircmps = []

    dircmps.append(dircmp)

    for sub_dircmp in dircmp.subdirs.values():
        dircmps.extend(_get_recursive_dircmps(sub_dircmp))

    return dircmps


def get_different_files_in_directories(
    left_directory_path: str, right_directory_path: str
) -> List[Tuple[str, str]]:
    """Get files with same name in both directories but with different contents or attributes.

    Files which are present in subdirectories that only exist in either the left
    or right directories are not returned. Use the 'get_directories_only_in_*_directory'
    functions to get subdirectories that are in either the left or right directories.
    This ensures that this function does not return individual files in whole new
    directories.
    """
    dircmps = _get_recursive_dircmps(
        filecmp.dircmp(left_directory_path, right_directory_path)
    )

    files = []

    for dircmp in dircmps:
        for diff_file in dircmp.diff_files:
            absolute_path_left = os.path.join(dircmp.left, diff_file)
            absolute_path_right = os.path.join(dircmp.right, diff_file)

            files.append((absolute_path_left, absolute_path_right))

    return files


def get_files_only_in_left_directory(
    left_directory_path: str, right_directory_path: str
) -> List[str]:
    """Get files which are only present in left directory.

    Files which are present in subdirectories that only exist in either the left
    or right directories are not returned. Use the 'get_directories_only_in_*_directory'
    functions to get subdirectories that are in either the left or right directories.
    This ensures that this function does not return individual files in whole new
    directories.
    """
    dircmps = _get_recursive_dircmps(
        filecmp.dircmp(left_directory_path, right_directory_path)
    )

    files = []

    for dircmp in dircmps:
        for left_only_file in dircmp.left_only:
            absolute_path = os.path.join(dircmp.left, left_only_file)

            if os.path.isdir(absolute_path):
                continue

            files.append(absolute_path)

    return files


def get_files_only_in_right_directory(
    left_directory_path: str, right_directory_path: str
) -> List[str]:
    """Get files which are only present in right directory.

    Files which are present in subdirectories that only exist in either the left
    or right directories are not returned. Use the 'get_directories_only_in_*_directory'
    functions to get subdirectories that are in either the left or right directories.
    This ensures that this function does not return individual files in whole new
    directories.
    """
    dircmps = _get_recursive_dircmps(
        filecmp.dircmp(left_directory_path, right_directory_path)
    )

    files = []

    for dircmp in dircmps:
        for right_only_file in dircmp.right_only:
            absolute_path = os.path.join(dircmp.right, right_only_file)

            if os.path.isdir(absolute_path):
                continue

            files.append(absolute_path)

    return files


def get_directories_only_in_left_directory(
    left_directory_path: str, right_directory_path: str
) -> List[str]:
    """Get directories which are only present in left directory."""
    dircmps = _get_recursive_dircmps(
        filecmp.dircmp(left_directory_path, right_directory_path)
    )

    directories = []

    for dircmp in dircmps:
        for left_only_file in dircmp.left_only:
            absolute_path = os.path.join(dircmp.left, left_only_file)

            if os.path.isfile(absolute_path):
                continue

            directories.append(absolute_path)

    return directories


def get_directories_only_in_right_directory(
    left_directory_path: str, right_directory_path: str
) -> List[str]:
    """Get directories which are only present in right directory."""
    dircmps = _get_recursive_dircmps(
        filecmp.dircmp(left_directory_path, right_directory_path)
    )

    directories = []

    for dircmp in dircmps:
        for right_only_file in dircmp.right_only:
            absolute_path = os.path.join(dircmp.right, right_only_file)

            if os.path.isfile(absolute_path):
                continue

            directories.append(absolute_path)

    return directories


def get_nested_directory_structure(
    paths_list: List[str],
) -> Dict[str, Optional[Dict[str, Optional[dict]]]]:
    """Convert list of paths to nested dict."""
    tree: Dict[str, Optional[Dict[str, Optional[dict]]]] = {}

    # Example of logic:
    #
    # >>> tree = {}
    # >>> node = tree
    # >>> node = node.setdefault('a', {})
    # >>> node = node.setdefault('b', {})
    # >>> node = tree
    # >>> tree
    # {'a': {'b': {}}}

    for path in paths_list:
        node = tree  # Reset to root level for new path, see docstring

        parts = Path(path).parts

        for i, element in enumerate(parts):
            last = i == (len(parts) - 1)

            if last:
                node.setdefault(element, None)
            else:
                node = node.setdefault(  # type: ignore[assignment]  # mypy does not support nested types
                    element, {}
                )  # Next recursion will be at this level, see docstring

    return tree
