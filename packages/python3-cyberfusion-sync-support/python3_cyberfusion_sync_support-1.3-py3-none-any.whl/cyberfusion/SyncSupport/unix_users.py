"""Classes for interaction with UNIX users."""

import getpass
import os
import shutil
import tarfile
from pathlib import Path, PosixPath
from typing import List, Optional, Tuple

from cached_property import cached_property

from cyberfusion.Common import generate_random_string, get_md5_hash
from cyberfusion.Common.FilesystemComparison import (
    get_directories_only_in_right_directory,
    get_files_only_in_right_directory,
)
from cyberfusion.SyncSupport import PATH_ARCHIVE
from cyberfusion.SyncSupport.exceptions import (
    FilesystemPathNotRelativeError,
    IllegalMemberError,
    StorePathNotRelativeError,
)


class UNIXUserHomeDirectoryArchive:
    """Abstraction of archive of UNIX user home directory."""

    EXTENSION_FILE_TAR_GZ = "tar.gz"

    def __init__(
        self,
        *,
        store_path: str,
        exclude_paths: Optional[List[str]] = None,
        archive_path_root_directory: str = PATH_ARCHIVE,
    ) -> None:
        """Set attributes.

        The archive is written to a file inside root_directory. The default path
        is are automatically cleaned up using systemd-tmpfiles, if this library
        is installed as a Debian package.
        """
        self.store_path = store_path
        self.exclude_paths = exclude_paths if exclude_paths is not None else []
        self.archive_path_root_directory = archive_path_root_directory

    @property
    def store_path(self) -> str:
        """Set store path.

        Path in archive is relative, so is path without leading slash.
        """
        return self._store_path

    @store_path.setter
    def store_path(self, value: str) -> None:
        """Set store path.

        Checks if store path is relative.
        """
        if os.path.isabs(value):
            raise StorePathNotRelativeError

        self._store_path = value

    @property
    def home_directory(self) -> Path:
        """Set home directory."""
        return Path.home()

    @property
    def username(self) -> str:
        """Set username."""
        return getpass.getuser()

    @cached_property
    def archive_path(self) -> str:
        """Set archive path."""
        user_directory = os.path.join(
            self.archive_path_root_directory,
            self.username,
        )

        os.makedirs(user_directory, exist_ok=True)

        return (
            os.path.join(
                user_directory,
                f"archive-{generate_random_string().lower()}",
            )
            + "."
            + self.EXTENSION_FILE_TAR_GZ
        )

    def create(self) -> Tuple[str, str]:
        """Create archive of store path."""

        # Create file with correct permissions

        with open(self.archive_path, "w"):
            pass

        os.chmod(self.archive_path, 0o600)

        # Create archive

        with tarfile.open(self.archive_path, "w:gz") as tar:
            tar.add(
                os.path.join(self.home_directory, self.store_path),
                filter=lambda x: None if x.name in self.exclude_paths else x,
                # self.store_path is relative to home directory, so this makes
                # paths inside the archive relative to home directory
                arcname=self.store_path,
            )

        return self.archive_path, get_md5_hash(self.archive_path)


class UNIXUserHomeDirectoryArchiveRestoration:
    """Abstraction of UNIX user home directory archive restore process.

    Restores path in archive to path on local filesystem.

    This function extracts the given path in the archive to a temporary directory.
    It then replaces the path on the local filesystem with the temporary directory.
    """

    # Ensure all restore-related directories start with this prefix. The prefix
    # might be used by other systems to recognise directories that are related
    # to an archive restore.

    PREFIX_RESTORE_FILESYSTEM_OBJECT = ".archive-restore-"

    def __init__(
        self,
        *,
        store_path: str,
        filesystem_path: str,
        archive_path: str,
        temporary_path_root_path: str,
        exclude_paths: Optional[List[str]] = None,
    ):
        """Set attributes."""
        self.archive_path = archive_path
        self.store_path = store_path
        self.filesystem_path = filesystem_path
        self.exclude_paths = exclude_paths if exclude_paths is not None else []
        self.temporary_path_root_path = temporary_path_root_path

    @property
    def filesystem_path(self) -> str:
        """Set filesystem path.

        Path on local filesystem is absolute, so is path with leading slash.
        """
        return self._filesystem_path

    @filesystem_path.setter
    def filesystem_path(self, value: str) -> None:
        """Set filesystem path.

        Path on local filesystem is absolute, so is path with leading slash.
        """
        if os.path.isabs(value):
            raise FilesystemPathNotRelativeError

        self._filesystem_path = os.path.join(self.home_directory, value)

    @property
    def store_path(self) -> str:
        """Set store path.

        Path in archive is relative, so is path without leading slash.
        """
        return self._store_path

    @store_path.setter
    def store_path(self, value: str) -> None:
        """Set store path.

        Checks if store path is relative.
        """
        if os.path.isabs(value):
            raise StorePathNotRelativeError

        self._store_path = value

    @property
    def home_directory(self) -> Path:
        """Set home directory."""
        return Path.home()

    @cached_property
    def temporary_path(
        self,
    ) -> str:
        """Generate and create temporary path."""
        temporary_path = os.path.join(
            self.temporary_path_root_path,
            self.PREFIX_RESTORE_FILESYSTEM_OBJECT
            + "tmp."
            + os.path.basename(self.filesystem_path)
            + "-"
            + generate_random_string(8),
        )

        os.mkdir(temporary_path)
        os.chmod(temporary_path, 0o700)

        return temporary_path

    @cached_property
    def old_path(self) -> str:
        """Set old path."""

        # Add dot prefix to prevent access, and add random string in case filesystem
        # object without random string already exists

        return os.path.join(
            Path(self.filesystem_path).parent,
            self.PREFIX_RESTORE_FILESYSTEM_OBJECT
            + "old."
            + os.path.basename(self.filesystem_path)
            + "-"
            + generate_random_string(8),
        )

    @cached_property
    def new_path(self) -> str:
        """Set new path."""

        # Add dot prefix to prevent access, and add random string in case filesystem
        # object without random string already exists

        return os.path.join(
            Path(self.filesystem_path).parent,
            self.PREFIX_RESTORE_FILESYSTEM_OBJECT
            + "new."
            + os.path.basename(self.filesystem_path)
            + "-"
            + generate_random_string(8),
        )

    def _extract(self) -> None:
        """Extract store path to temporary path."""
        tar = tarfile.open(self.archive_path)

        # As the entire archive is extracted by tar.extractall, we must check
        # here that the archive contains only expected members, i.e. those in
        # the store path. If the archive contains any member that is not in
        # the given store path, an exception will be raised instead of silently
        # continuing because, when creating the archive with UNIXUserHomeDirectoryArchive,
        # this should never happen.

        for member in tar.getmembers():
            # Member *is* the store path itself, which is the only member
            # allowed outside of the store path

            if member.name == self.store_path:
                continue

            # Member is inside the given store path

            if Path(self.store_path) in PosixPath(member.name).parents:
                continue

            raise IllegalMemberError(member.name)

        # Extract entire archive

        tar.extractall(self.temporary_path)

        tar.close()

    @property
    def username(self) -> str:
        """Set username."""
        return getpass.getuser()

    def _copy(self) -> None:
        """Copy files that are in the filesystem path but not in the archive (i.e. removed) and are excluded (excluding excludes from deletion)."""
        for f in get_files_only_in_right_directory(
            os.path.join(self.temporary_path, self.store_path),
            self.filesystem_path,
        ):
            if os.path.relpath(f, self.home_directory) not in self.exclude_paths:
                continue

            destination_path = os.path.join(
                self.temporary_path,
                self.store_path,
                os.path.relpath(f, self.filesystem_path),
            )

            shutil.copyfile(f, destination_path)

        for f in get_directories_only_in_right_directory(
            os.path.join(self.temporary_path, self.store_path),
            self.filesystem_path,
        ):
            if os.path.relpath(f, self.home_directory) not in self.exclude_paths:
                continue

            destination_path = os.path.join(
                self.temporary_path,
                self.store_path,
                os.path.relpath(f, self.filesystem_path),
            )

            shutil.copytree(f, destination_path, ignore_dangling_symlinks=True)

    def replace(self) -> None:
        """Replace object on local filesystem with object from archive.

        This is a nearly atomic process. I.e. there is almost no downtime when
        replacing.
        """

        # Extract archive. The filesystem path remains untouched until this is
        # completed. This ensures that the filesystem is not left in a broken
        # state if the extraction fails.

        self._extract()

        # Copy deleted files that were excluded

        if os.path.lexists(self.filesystem_path):
            self._copy()

        # Move the extracted filesystem objects to the new path. As these may be
        # on different filesystems, the move could take a while. We restore to the
        # new path instead of to the filesystem path. If we restored to the filesystem
        # path, we would have to get the original filesystem object out of the way,
        # leaving the filesystem structure in a 'broken' state, while the move could
        # take a while. In order to prevent downtime, we restore to this temporary
        # new directory first.

        shutil.move(
            os.path.join(self.temporary_path, self.store_path),
            self.new_path,
        )

        # If the filesystem path already exists, move it out of the way so that
        # we can move the new path to it. This procedure is also followed for
        # regular files. Unlike non-empty directories, regular files can be
        # overwritten without having to ensure the filesystem object does not
        # exist at the path, unless the regular file is write-protected (e.g.
        # if it has permissions 0400).

        if os.path.lexists(self.filesystem_path):
            os.rename(self.filesystem_path, self.old_path)

        # Move the new path to the filesystem path. This completes the restore.

        os.rename(self.new_path, self.filesystem_path)

        # Remove the old path if it exists (it exists if the filesystem path
        # existed before doing the restore, see above).

        if os.path.lexists(self.old_path):
            shutil.rmtree(self.old_path)
