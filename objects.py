import hashlib
from typing import Tuple


def hash_blob(content) -> str:
    """
    Return the 40-char hex SHA-1 git would assign to this content as a blob.
    Format: "blob <byte_len>\0<content>" then SHA-1.
    """
    header = f"blob {len(content)}\0"
    data = header + content
    return hashlib.sha1(data.encode("ascii")).hexdigest()


VALID_TYPES = {"blob", "tree", "commit", "tag"}
def parse_object(raw: str) -> Tuple[str, str, str]:
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