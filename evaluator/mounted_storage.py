from __future__ import annotations

import fcntl
import json
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class MountedStorage:
    def __init__(self) -> None:
        self.root = self.resolve_root()
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def resolve_root() -> Path:
        configured = os.environ.get("EVAL_DATA_ROOT")
        if configured:
            return Path(configured).resolve()
        relative_mount = Path("data")
        if relative_mount.exists():
            return relative_mount.resolve()
        absolute_mount = Path("/data")
        if absolute_mount.exists():
            return absolute_mount.resolve()
        return absolute_mount.resolve()

    def path(self, relative_path: str) -> Path:
        path = (self.root / relative_path).resolve()
        if self.root not in path.parents and path != self.root:
            raise ValueError(f"Path escapes EVAL_DATA_ROOT: {relative_path}")
        return path

    @contextmanager
    def lock(self, name: str = "metadata/evaluator.lock") -> Iterator[None]:
        lock_path = self.path(name)
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def read_json(self, relative_path: str, default: Any) -> Any:
        path = self.path(relative_path)
        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def write_json(self, relative_path: str, value: Any) -> None:
        path = self.path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(path.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temp_path.replace(path)

    def copy_file(self, source_path: str | Path, relative_path: str) -> Path:
        destination = self.path(relative_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination)
        return destination
