#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

CHUNK_SIZE = 1024 * 1024

# Matches a UUID prefix followed by an underscore, e.g.
# "4d391215-6e1f-43c7-aad9-80fa67349ab1_"
_UUID_PREFIX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}_",
    re.IGNORECASE,
)


def canonical_name(filename: str) -> str:
    """Return the filename with a leading UUID prefix removed, if present."""
    return _UUID_PREFIX.sub("", filename)


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
    seen_hashes: dict[str, Path] = {}
    seen_names: dict[str, Path] = {}
    deleted = 0

    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue

        try:
            digest = file_hash(path)
        except OSError as error:
            print(f"Skipped unreadable file: {path.name} ({error})", file=sys.stderr)
            continue

        name = canonical_name(path.name)

        hash_original = seen_hashes.get(digest)
        name_original = seen_names.get(name)
        original = hash_original if hash_original is not None else name_original
        if original is not None:
            try:
                path.unlink()
            except OSError as error:
                print(f"Could not delete duplicate: {path.name} ({error})", file=sys.stderr)
                continue
            deleted += 1
            print(f"Deleted duplicate: {path.name} (same as {original.name})")
        else:
            seen_hashes[digest] = path
            seen_names[name] = path

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
