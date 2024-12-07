"""Helper classes for Cyberfusion scripts."""

import base64
import os
import secrets
import shutil
import string
import uuid
from datetime import datetime, timezone
from hashlib import md5, sha1
from socket import gethostname
from typing import Optional

import requests

from cyberfusion.Common.exceptions import ExecutableNotFound

CHAR_PREFIX_WILDCARD = "*"
CHAR_LABEL = "."


class EmailAddresses:
    """Cyberfusion email addresses."""

    SYSTEM_MESSAGES_CORE = "system-messages.core@cyberfusion.io"
    SYSTEM_MESSAGES_INFRASTRUCTURE = "system-messages.infrastructure@cyberfusion.io"
    SUPPORT = "support@cyberfusion.io"


def find_executable(name: str) -> str:
    """Find absolute path of executable.

    Use this function when the executable must exist. This function raises an
    exception if it does not.
    """
    path = shutil.which(name)

    if path:
        return path

    raise ExecutableNotFound(name)


def try_find_executable(name: str) -> Optional[str]:
    """Find absolute path of executable.

    Use this function when the executable may be absent. This function returns
    None if it is.
    """
    return shutil.which(name)


def download_from_url(url: str, *, root_directory: Optional[str] = None) -> str:
    """Download from URL.

    Large files are supported due to use of chunking and streaming.

    Inspired by https://stackoverflow.com/a/16696317/19535769
    """
    if root_directory is None:
        root_directory = os.path.join(os.path.sep, "tmp")

    path = os.path.join(root_directory, generate_random_string())

    # Create and set permissions

    with open(path, "w"):
        pass

    os.chmod(path, 0o600)

    # Download

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return path


def get_tmp_file() -> str:
    """Create tmp file and return path."""
    path = os.path.join(os.path.sep, "tmp", str(uuid.uuid4()))

    with open(path, "w"):
        pass

    os.chmod(path, 0o600)  # Do not allow regular users to view file contents

    return path


def get_hostname() -> str:
    """Get hostname."""
    return gethostname()


def get_domain_is_wildcard(domain: str) -> bool:
    """Determine if domain is wildcard."""
    return domain.split(CHAR_LABEL)[0] == CHAR_PREFIX_WILDCARD


def get_today_timestamp() -> float:
    """Get UNIX timestamp from the first second of today."""
    current_datetime = datetime.utcnow()

    return (
        datetime(
            year=current_datetime.year,
            month=current_datetime.month,
            day=current_datetime.day,
        )
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )


def generate_random_string(length: int = 24) -> str:
    """Generate random string."""

    # Set allowed characters (ASCII + digits)

    alphabet = string.ascii_letters + string.digits

    # Return string using allowed characters

    return "".join(secrets.choice(alphabet) for i in range(length))


def hash_string_mariadb(string: str) -> str:
    """Hash string with SHA-1 by MariaDB standards."""
    return (
        "*"
        + sha1(sha1(string.encode("utf-8")).digest())  # noqa: S303
        .hexdigest()
        .upper()
    )


def convert_bytes_gib(size: int) -> float:
    """Convert bytes to GiB."""
    return size / (1024**3)


def get_md5_hash(path: str) -> str:
    """Get Base64 encoded 128-bit MD5 digest of file."""
    hash_ = md5()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash_.block_size), b""):
            hash_.update(chunk)

    return base64.b64encode(hash_.digest()).decode()


def ensure_trailing_newline(text: str) -> str:
    """Add trailing newline to text if missing."""
    if not text.endswith("\n"):
        return text + "\n"

    return text
