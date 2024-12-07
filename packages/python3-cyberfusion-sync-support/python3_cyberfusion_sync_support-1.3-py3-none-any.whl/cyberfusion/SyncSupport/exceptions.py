"""Exceptions."""

from dataclasses import dataclass


class SyncSupportError(Exception):
    """Error occurred using this library."""

    pass


@dataclass
class IllegalMemberError(SyncSupportError):
    """Archive contains member that is not in store path."""

    member_name: str


class StorePathNotRelativeError(SyncSupportError):
    """Store path is not relative (to UNIX user home directory)."""

    pass


class FilesystemPathNotRelativeError(SyncSupportError):
    """Filesystem path is not relative (to UNIX user home directory)."""

    pass
