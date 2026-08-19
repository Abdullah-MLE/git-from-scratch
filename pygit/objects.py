import hashlib
from typing import Tuple

VALID_TYPES = {"blob", "tree", "commit", "tag"}


def hash_object(obj_type: str, content: str | bytes) -> str:
    """Compute a SHA-1 hash for a Git object and its content."""
    content_bytes = content.encode("utf-8") if isinstance(content, str) else content
    header = f"{obj_type} {len(content_bytes)}\0".encode("utf-8")
    data = header + content_bytes
    return hashlib.sha1(data).hexdigest()


def parse_object(raw: str) -> Tuple[str, str, str]:
    """Parse and validate a serialized Git object."""
    sep = "\\0"
    sep_location = raw.find(sep)
    if sep_location == -1:
        raise ValueError("ERR no NUL separator")

    header = raw[:sep_location]
    body = raw[sep_location + len(sep):]

    if " " not in header:
        raise ValueError("ERR invalid header format")

    obj_type, size = header.split(" ", 1)

    if obj_type not in VALID_TYPES:
        raise ValueError(f"ERR unknown type {obj_type}")

    if not size.isdigit() or int(size) != len(body):
        raise ValueError("ERR size is not correct!")

    return obj_type, size, body


def get_object_path(sha: str) -> str:
    """Build the loose-object path for a given SHA-1."""
    return f".git/objects/{sha[:2]}/{sha[2:]}"