import os
import shutil
import pathlib
from typing import List, Optional, Union

__all__ = ['PathBuf']


class PathBuf:
    def __init__(self, path: Union[str, os.PathLike, None] = None):
        """
        Initialize a PathBuf object.

        :param path: Optional initial path. If None, creates an empty path.
        """
        self._path = pathlib.Path(path) if path is not None else pathlib.Path()

    @classmethod
    def new_from_append(cls, s: str) -> 'PathBuf':
        """
        Creates a new PathBuf by starting from the root directory and appending the given string.

        :param s: String to append to the root path
        :return: New PathBuf instance
        """
        return cls(os.path.sep + s)

    @classmethod
    def new_from_home_dir(cls) -> 'PathBuf':
        """
        Creates a new PathBuf pointing to the user's home directory.

        :return: PathBuf for home directory
        """
        return cls(os.path.expanduser('~'))

    @classmethod
    def new_from_documents_dir(cls) -> 'PathBuf':
        """
        Creates a new PathBuf pointing to the user's documents directory.

        :return: PathBuf for documents directory
        """
        return cls(os.path.expanduser('~/Documents'))

    @classmethod
    def new_from_desktop_dir(cls) -> 'PathBuf':
        """
        Creates a new PathBuf pointing to the user's desktop directory.

        :return: PathBuf for desktop directory
        """
        return cls(os.path.expanduser('~/Desktop'))

    @classmethod
    def new_from_default_apollo_robots_dir(cls) -> 'PathBuf':
        """
        Creates a new PathBuf pointing to the default Apollo robots directory.

        :return: PathBuf for Apollo robots directory
        :raises AssertionError: If the directory does not exist
        """
        path = cls.new_from_documents_dir().append('apollo-resources/robots')
        assert path.exists(), f"Default apollo robots dir path {path} does not exist."
        return path

    @classmethod
    def new_from_default_apollo_environments_dir(cls) -> 'PathBuf':
        """
        Creates a new PathBuf pointing to the default Apollo environments directory.

        :return: PathBuf for Apollo environments directory
        :raises AssertionError: If the directory does not exist
        """
        path = cls.new_from_documents_dir().append('apollo-resources/environments')
        assert path.exists(), f"Default apollo environments dir path {path} does not exist."
        return path

    def append(self, s: str) -> 'PathBuf':
        """
        Appends a string to the current path, handling both Unix and Windows path separators.

        :param s: String to append
        :return: New PathBuf with appended path
        """
        # Check for both Unix and Windows path separators
        if '/' in s and '\\' in s:
            raise ValueError("Cannot have both / and \\ in append")

        # Split the string by path separators and join
        parts = s.replace('\\', '/').split('/')
        new_path = self._path
        for part in parts:
            if part:
                new_path = new_path / part

        return PathBuf(new_path)

    def append_vec(self, v: List[str]) -> 'PathBuf':
        """
        Appends multiple strings from a list to the current path.

        :param v: List of strings to append
        :return: New PathBuf with appended paths
        """
        result = self
        for s in v:
            result = result.append(s)
        return result

    def append_without_separator(self, s: str) -> 'PathBuf':
        """
        Appends a string to the current path without using a path separator.

        :param s: String to append
        :return: New PathBuf with appended string
        """
        return PathBuf(str(self._path) + s)

    def append_path(self, other: 'PathBuf') -> 'PathBuf':
        """
        Appends another PathBuf to the current path.

        :param other: PathBuf to append
        :return: New PathBuf with appended path
        """
        return self.append(str(other._path))

    def split_into_strings(self) -> List[str]:
        """
        Splits the path into a list of path components as strings.

        :return: List of path components
        """
        return [part for part in self._path.parts if part]

    def split_into_path_bufs(self) -> List['PathBuf']:
        """
        Splits the path into a list of PathBufs.

        :return: List of PathBufs representing path components
        """
        return [PathBuf(part) for part in self._path.parts if part]

    def walk_directory_and_find_first(self, s: Union[str, 'PathBuf']) -> 'PathBuf':
        """
        Recursively walks a directory and finds the first file matching the path.

        :param s: Path or filename to find
        :return: PathBuf of the first matching file
        :raises RuntimeError: If file is not found
        """
        search_path = s._path if isinstance(s, PathBuf) else pathlib.Path(s)

        for root, _, files in os.walk(self._path):
            for file in files:
                full_path = pathlib.Path(root) / file
                if full_path.name == search_path.name:
                    return PathBuf(full_path)

        raise RuntimeError(f"Could not find {search_path}")

    def walk_directory_and_find_all(self, s: Union[str, 'PathBuf']) -> List['PathBuf']:
        """
        Recursively walks a directory and finds all files matching the path.

        :param s: Path or filename to find
        :return: List of PathBufs of matching files
        """
        search_path = s._path if isinstance(s, PathBuf) else pathlib.Path(s)

        results = []
        for root, _, files in os.walk(self._path):
            for file in files:
                full_path = pathlib.Path(root) / file
                if full_path.name == search_path.name:
                    results.append(PathBuf(full_path))

        return results

    def create_directory(self):
        """
        Creates the directory if it does not exist.
        """
        os.makedirs(self._path, exist_ok=True)

    def delete_file(self):
        """
        Deletes the file at the current path.
        """
        os.remove(self._path)

    def delete_directory(self):
        """
        Deletes the directory at the current path.
        """
        shutil.rmtree(self._path)

    def delete_all_items_in_directory(self):
        """
        Deletes all items within the directory and recreates it.
        """
        self.delete_directory()
        self.create_directory()

    def copy_file_to_destination_file_path(self, destination: 'PathBuf'):
        """
        Copies a file to a destination file path.

        :param destination: Destination PathBuf
        """
        assert self._path.is_file(), "Source must be a file"

        # Ensure destination directory exists
        destination._path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(self._path, destination._path)

    def copy_file_to_destination_directory(self, destination: 'PathBuf'):
        """
        Copies a file to a destination directory.

        :param destination: Destination directory PathBuf
        """
        assert self._path.is_file(), "Source must be a file"

        destination.create_directory()
        dest_file = destination.append(self._path.name)
        shutil.copy2(self._path, dest_file._path)

    def extract_last_n_segments(self, n: int) -> 'PathBuf':
        """
        Extracts the last n path segments.

        :param n: Number of segments to extract
        :return: New PathBuf with last n segments
        """
        assert n > 0, "n must be greater than 0"

        parts = list(self._path.parts)
        n = min(n, len(parts))
        return PathBuf(os.path.join(*parts[-n:]))

    def get_all_items_in_directory(
            self,
            include_directories: bool = True,
            include_hidden_directories: bool = False,
            include_files: bool = True,
            include_hidden_files: bool = False
    ) -> List['PathBuf']:
        """
        Retrieves all items in a directory with various filtering options.

        :param include_directories: Include directories
        :param include_hidden_directories: Include hidden directories
        :param include_files: Include files
        :param include_hidden_files: Include hidden files
        :return: List of PathBufs for items in the directory
        """
        results = []

        try:
            for item in os.scandir(self._path):
                is_hidden = item.name.startswith('.')

                if item.is_dir():
                    if include_directories and (include_hidden_directories or not is_hidden):
                        results.append(PathBuf(item.path))

                if item.is_file():
                    if include_files and (include_hidden_files or not is_hidden):
                        results.append(PathBuf(item.path))

        except PermissionError:
            # Handle permission errors gracefully
            pass

        return results

    def get_all_filenames_in_directory(self, include_hidden_files: bool = False) -> List[str]:
        """
        Retrieves all filenames in a directory.

        :param include_hidden_files: Include hidden files
        :return: List of filenames
        """
        items = self.get_all_items_in_directory(False, False, True, include_hidden_files)
        return [item._path.name for item in items]

    def read_file_contents_to_string(self) -> str:
        """
        Reads file contents to a string.

        :return: File contents as a string
        """
        with open(self._path, 'r') as f:
            return f.read()

    def write_string_to_file(self, s: str):
        """
        Writes a string to a file.

        :param s: String to write
        """
        # Ensure parent directory exists
        self._path.parent.mkdir(parents=True, exist_ok=True)

        # Remove existing file if it exists
        if self._path.exists():
            self._path.unlink()

        with open(self._path, 'w') as f:
            f.write(s)

    def verify_extension(self, extensions: List[str]) -> Optional[bool]:
        """
        Verifies that the file has one of the specified extensions.

        :param extensions: List of allowed extensions
        :return: True if extension matches, None otherwise
        :raises ValueError: If no extension matches
        """
        ext = self._path.suffix.lstrip('.')
        if ext in extensions:
            return True
        raise ValueError(f"Path {self._path} does not have one of the following extensions: {extensions}")

    def exists(self) -> bool:
        """
        Checks if the path exists.

        :return: True if path exists, False otherwise
        """
        return self._path.exists()

    def to_string(self):
        return str(self._path)

    def __str__(self) -> str:
        """
        Returns string representation of the path.

        :return: Path as a string
        """
        return str(self._path)

    def __repr__(self) -> str:
        """
        Returns detailed string representation.

        :return: Detailed path representation
        """
        return f"PathBuf({str(self._path)})"
