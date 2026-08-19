from typing import Iterable, List, Tuple

from .objects import hash_object


TreeEntry = Tuple[str, str, str]


def build_tree_body(entries: Iterable[TreeEntry]) -> bytes:
    """Build the binary body of a tree object from its entries."""
    sorted_entries = sorted(entries, key=lambda entry: entry[1].encode("utf-8"))
    body = bytearray()

    for mode, name, object_sha in sorted_entries:
        body.extend(f"{mode} {name}\0".encode("utf-8"))
        body.extend(bytes.fromhex(object_sha))

    return bytes(body)


def hash_tree(entries: Iterable[TreeEntry]) -> str:
    """Build a tree object and return its SHA-1 hash."""
    return hash_object("tree", build_tree_body(entries))


def parse_tree_entries(lines: Iterable[str]) -> List[TreeEntry]:
    """Parse tree entries from the lesson's line-based input format."""
    input_lines = list(lines)
    if not input_lines:
        return []

    count = int(input_lines[0])
    entries = []
    for line in input_lines[1:count + 1]:
        mode, name, object_sha = line.split(" ")
        entries.append((mode, name, object_sha))
    return entries


def run_tree_hash(lines: Iterable[str]) -> str:
    """Parse tree input and return the tree object's SHA-1 hash."""
    return hash_tree(parse_tree_entries(lines))