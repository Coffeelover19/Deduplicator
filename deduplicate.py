#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
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

        try:
            digest = file_hash(path)
        except OSError as error:
            print(f"Skipped unreadable file: {path.name} ({error})", file=sys.stderr)
            continue

        if digest in seen:
            try:
                path.unlink()
            except OSError as error:
                print(f"Could not delete duplicate: {path.name} ({error})", file=sys.stderr)
                continue
            deleted += 1
            print(f"Deleted duplicate: {path.name} (same as {seen[digest].name})")
        else:
            seen[digest] = path

    return deleted


def main() -> int:
    working_dir = Path.cwd()
    try:
        deleted = deduplicate(working_dir)
    except OSError as error:
        print(f"Error while deduplicating files: {error}", file=sys.stderr)
        return 1
    noun = "file" if deleted == 1 else "files"
    print(f"Done. Deleted {deleted} duplicate {noun}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
