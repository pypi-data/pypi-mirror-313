"""Helper for handling filesystem."""

import os
from enum import Enum
from pathlib import Path

import psutil

CEPH_NAME_ATTRIBUTE_RBYTES = "ceph.dir.rbytes"


class FilesystemType(Enum):
    """Filesystem types.

    We don't expect any other filesystems than the ones in this Enum under normal
    circumstances. This Enum prevents you from having to write filesystem types
    by name manually; it's not a complete list of all possibilities.
    """

    EXT4 = "ext4"
    EXT2 = "ext2"  # Usually for /boot
    XFS = "xfs"
    CEPH = "ceph"
    OVERLAY = "overlay"  # Usually for Docker
    APFS = "apfs"  # Development on macOS


def get_filesystem(path: str) -> str:
    """Get filesystem that absolute path is on.

    Returns the earliest filesystem. E.g. if '/a/b/c' is passed, and both '/a' and
    '/b' are mountpoints, '/b' is returned.

    Does not resolve symlinks, so the filesystem of the symlink itself is looked
    up.

    Inspired by https://stackoverflow.com/a/4453715/3837431
    """

    # Ensure path is an absolute path. For relative paths, dirname() would return
    # the wrong result

    path = os.path.abspath(path)

    # Work our way down the path by getting the directory that the current
    # filesystem object is in

    while not os.path.ismount(path):
        path = os.path.dirname(path)

    return path


def get_filesystem_type(path: str) -> FilesystemType:
    """Get type of filesystem."""

    # If this yields no results (i.e. the path is missing), next() raises StopIteration

    partition = next(
        filter(lambda x: x.mountpoint == path, psutil.disk_partitions(all=True))
    )

    return FilesystemType(partition.fstype)


def get_directory_size(path: str) -> int:
    """Get size of directory."""

    # CephFS is a special case, as CephFS has extended attributes to determine
    # size

    is_ceph = get_filesystem_type(get_filesystem(path)) == FilesystemType.CEPH

    if is_ceph:
        return int(os.getxattr(path, CEPH_NAME_ATTRIBUTE_RBYTES).decode("utf-8"))  # type: ignore[attr-defined]

    # Loop through directory for filesystems without special implementation

    return sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())
