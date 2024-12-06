from functools import partial
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from shutil import copy2
from sys import modules
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from typing import Callable, Optional

from joblib import Parallel, delayed
from tqdm import tqdm

# noinspection PyProtectedMember
from .tools import convert
from .types import File, Folder

"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// User Interactions
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


def select_file(**kwargs) -> Path:
    """
    Interactive tool for file selection. All keyword arguments are
    passed to `tkinter.filedialog.askopenfilename <https://docs.python.org/3/library/tk.html>`_

    :param kwargs: keyword arguments passed to tkinter.filedialog.askdirectory

    :raises: FileNotFoundError if file not found

    :return: absolute path to file
    """
    root = Tk()
    file_path = Path(askopenfilename(**kwargs))
    root.destroy()

    if str(file_path) == ".":
        raise FileNotFoundError(f"File not found: {file_path}")

    return file_path.resolve()


def select_directory(**kwargs) -> Path:
    """
    Interactive tool for directory selection. All keyword arguments are
    passed to `tkinter.filedialog.askdirectory <https://docs.python.org/3/library/tk.html>`_

    :param kwargs: keyword arguments passed to tkinter.filedialog.askdirectory

    :raises: FileNotFoundError if directory not found

    :return: absolute path to directory
    """
    root = Tk()
    directory_path = Path(askdirectory(**kwargs))
    root.destroy()

    if str(directory_path) == ".":
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    return directory_path.resolve()


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// File Operations
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


@convert(parameter="source", permitted=(Folder,), required=Path)
@convert(parameter="destination", permitted=(Folder,), required=Path)
def verbose_copy(source: Folder,
                 destination: Folder,
                 feedback: Optional[str] = None) -> bool:
    """
    Copy a file from source to destination. If verbose is True, print feedback.

    :param source: source file path
    :type source: :class:`str` or :class:`Path <pathlib.Path>`

    :param destination: destination file path
    :type destination: :class:`str` or :class:`Path <pathlib.Path>`

    :param feedback: feedback message
    :type feedback: :class:`Optional <typing.Optional>`\[:class:`str`\], default: ``None``

    :return: True if successful, False otherwise
    """
    # Verbose, performant copying by parallelizing the copy operation. This is faster than the built-in shutil.copytree.
    # Implemented by making a partial containing the source & destination paths, and the fast-copy function for the OS.
    # Joblib will handle the parallelization when provided the partial via 'delayed'. Loky seems to be the fastest for
    # moving many small files, but threading could be faster in other scenarios. I don't see a user providing enough
    # file paths they run out of system RAM, so not exposing the joblib backend to allow threading as an alternative.
    # The list of the file paths is wrapped in tqdm to provide verbose feedback (progress bar).

    def _copy(source_: Path, destination_: Path, file: Path) -> Path:  # pragma: no cover
        """
        Copy a file from source to destination (single file function, parallelized). Should call the system fast-copy
        regardless of the OS.
        """
        file_destination = destination_.joinpath(file.relative_to(source_))
        return copy2(file, file_destination)

    destination.mkdir(parents=True, exist_ok=True)
    folders = [folder for folder in source.rglob("*") if not folder.is_file()]
    destination.mkdir(parents=True, exist_ok=True)
    for folder in folders:
        destination_folder = destination.joinpath(folder.relative_to(source))
        destination_folder.mkdir(parents=True, exist_ok=True)

    files = [file for file in source.rglob("*") if file.is_file()]
    copier = partial(_copy, source, destination)
    message = f"Copying {feedback} files" if feedback else "Copying files"
    return all(Parallel(n_jobs=-1, backend="threading")(delayed(copier)(file) for file in tqdm(files,
                                                                                               total=len(files),
                                                                                               desc=message)))


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Importing
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
"""


@convert(parameter="path", permitted=(File,), required=Path)
def import_callable_from_file(name: str, module: str, path: File) -> Callable:
    spec = spec_from_file_location(module, path)
    module_ = module_from_spec(spec)
    modules[module] = module_
    spec.loader.exec_module(module_)
    return getattr(module_, name)


def import_function_from_file(name: str, file: Path) -> Callable:
    """
    Import a function from a file

    :param name: name of the function

    :param file: path to the file

    :return: function
    """
    spec = spec_from_file_location(name, file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, name)
