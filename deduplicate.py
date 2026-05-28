#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def deduplicate(directory: Path) -> int:
    seen: dict[str, Path] = {}
    deleted = 0

    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue

        digest = file_hash(path)
        if digest in seen:
            path.unlink()
            deleted += 1
            print(f"Deleted duplicate: {path.name} (same as {seen[digest].name})")
        else:
            seen[digest] = path

    return deleted


def main() -> int:
    working_dir = Path.cwd()
    deleted = deduplicate(working_dir)
    print(f"Done. Deleted {deleted} duplicate file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
