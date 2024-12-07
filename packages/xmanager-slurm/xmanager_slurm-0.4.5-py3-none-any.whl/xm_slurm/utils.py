import functools
import os
import pathlib
import sys
from typing import Callable, Hashable, Iterable, MutableSet, TypeVar

T = TypeVar("T")


class UserSet(Hashable, MutableSet[T]):
    __hash__ = MutableSet._hash

    def __init__(
        self,
        iterable: Iterable[T] = (),
        /,
        on_add: Callable[[T], None] = lambda x: None,
        on_remove: Callable[[T], None] = lambda x: None,
        on_discard: Callable[[T], None] = lambda x: None,
    ):
        self.data = set(iterable)
        self._on_add = on_add
        self._on_remove = on_remove
        self._on_discard = on_discard

    def __contains__(self, value):
        return value in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

    def add(self, value: T):
        self.data.add(value)
        self._on_add(value)

    def remove(self, value: T):
        self.data.remove(value)
        self._on_remove(value)

    def discard(self, value: T):
        self.data.discard(value)
        self._on_discard(value)


@functools.cache
def find_project_root() -> pathlib.Path:
    launch_script_path: pathlib.Path | None = None
    launch_script_path = pathlib.Path(sys.argv[0])

    if sys.argv[0].endswith(".py"):
        launch_script_path = pathlib.Path(sys.argv[0]).resolve()
    else:
        main_file_path = getattr(sys.modules["__main__"], "__file__", None)
        if main_file_path and os.access(main_file_path, os.R_OK):
            launch_script_path = pathlib.Path(main_file_path).resolve()

    pdir = launch_script_path.parent if launch_script_path else pathlib.Path.cwd().resolve()
    while pdir != pdir.parent:
        if (
            (pdir / "pyproject.toml").exists()
            or (pdir / "setup.py").exists()
            or (pdir / "setup.cfg").exists()
            or (pdir / "requirements.txt").exists()
            or (pdir / "requirements.in").exists()
            or (pdir / "uv.lock").exists()
            or (pdir / ".venv").exists()
        ):
            return pdir
        pdir = pdir.parent

    raise RuntimeError(f"Could not find project root from {sys.argv[0]}. Please specify `context`.")
