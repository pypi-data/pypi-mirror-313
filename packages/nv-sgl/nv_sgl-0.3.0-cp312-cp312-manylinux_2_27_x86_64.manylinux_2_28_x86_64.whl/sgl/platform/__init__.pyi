from collections.abc import Sequence
import pathlib
from typing import overload


class FileDialogFilter:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, name: str, pattern: str) -> None: ...

    @overload
    def __init__(self, arg: tuple[str, str], /) -> None: ...

    @property
    def name(self) -> str:
        """Readable name (e.g. "JPEG")."""

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def pattern(self) -> str:
        """File extension pattern (e.g. "*.jpg" or "*.jpg,*.jpeg")."""

    @pattern.setter
    def pattern(self, arg: str, /) -> None: ...

class MemoryStats:
    @property
    def rss(self) -> int:
        """Current resident/working set size in bytes."""

    @property
    def peak_rss(self) -> int:
        """Peak resident/working set size in bytes."""

def app_data_directory() -> pathlib.Path:
    """The application data directory."""

def choose_folder_dialog() -> pathlib.Path | None:
    """
    Show a folder selection dialog.

    Returns:
        The selected folder path or nothing if the dialog was cancelled.
    """

def display_scale_factor() -> float:
    """The pixel scale factor of the primary display."""

def executable_directory() -> pathlib.Path:
    """The current executable directory."""

def executable_name() -> str:
    """The current executable name."""

def executable_path() -> pathlib.Path:
    """The full path to the current executable."""

def home_directory() -> pathlib.Path:
    """The home directory."""

def memory_stats() -> MemoryStats:
    """Get the current memory stats."""

def open_file_dialog(filters: Sequence[FileDialogFilter] = []) -> pathlib.Path | None:
    """
    Show a file open dialog.

    Parameter ``filters``:
        List of file filters.

    Returns:
        The selected file path or nothing if the dialog was cancelled.
    """

page_size: int = 4096

def project_directory() -> pathlib.Path:
    """
    The project source directory. Note that this is only valid during
    development.
    """

def runtime_directory() -> pathlib.Path:
    """
    The runtime directory. This is the path where the sgl runtime library
    (sgl.dll, libsgl.so or libsgl.dynlib) resides.
    """

def save_file_dialog(filters: Sequence[FileDialogFilter] = []) -> pathlib.Path | None:
    """
    Show a file save dialog.

    Parameter ``filters``:
        List of file filters.

    Returns:
        The selected file path or nothing if the dialog was cancelled.
    """
