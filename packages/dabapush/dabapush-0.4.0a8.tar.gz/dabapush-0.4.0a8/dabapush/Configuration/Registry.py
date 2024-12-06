"""fetching plug-ins from entrypoints and helper methods"""

# pylint: disable=W0622
import platform
from importlib.metadata import EntryPoint
from typing import Any, List, Optional, Type

from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


def _get_entrypoint_py38(group: str) -> List[EntryPoint]:
    from importlib.metadata import entry_points  # pylint: disable=C0415

    return entry_points()[group]


def _get_entrypoint_py39(group: str) -> List[EntryPoint]:
    from importlib.metadata import entry_points  # pylint: disable=C0415

    return list(entry_points().select(group=group))


py_major, py_minor, _ = platform.python_version_tuple()

if int(py_major) == 3 and int(py_minor) == 8:
    _get_entrypoint = _get_entrypoint_py38
else:
    _get_entrypoint = _get_entrypoint_py39


def readers() -> List[EntryPoint]:
    """fetch readers from entry point"""
    return _get_entrypoint("dabapush_readers")


def writers() -> List[EntryPoint]:
    """fetch writers from entry point"""
    return _get_entrypoint("dabapush_writers")


def get_reader(name: str) -> Optional[Type[ReaderConfiguration]]:
    """
    params:
      name: str:
        registry key to retrieve
    returns:
        ReaderConfiguration or None: the requested ReaderConfiguration or None if
        no matching configuration is found.
    """
    candidates = [_ for _ in readers() if _.name == name]
    try:
        return candidates[0].load()
    except IndexError:
        return None


def get_writer(name: str) -> Optional[Type[WriterConfiguration]]:
    """
    params:
      name: str:
        registry key to retrieve
    returns:
        WriterConfiguration or None: the requested WriterConfiguration or None if
        no matching configuration is found."""
    candidates = [_ for _ in writers() if _.name == name]
    try:
        return candidates[0].load()
    except IndexError:
        return None


def __ensure_reader__(arg: Any) -> bool:
    return issubclass(arg, ReaderConfiguration)


def __ensure_writer__(arg: Any) -> bool:
    return issubclass(arg, WriterConfiguration)


def list_all_readers() -> List[str]:
    """return a list of all readers"""
    return [_.name for _ in readers()]


def list_all_writers() -> List[str]:
    """return a list of all writers"""

    return [_.name for _ in writers()]
