import sys, hashlib

# Compute git's "blob" SHA-1 over the content of each input line.
# Format: "blob <byte_len>\0<content>" then SHA-1.

# Parse a single inflated git object: "<type> <size>\0<body>".
# The test feeds the NUL placeholder as the literal two characters "\\0".

def hash_blob(content: bytes) -> str:
    """Return the 40-char hex SHA-1 git would assign to this content as a blob."""
    header = f"blob {len(content)}\0".encode("ascii")
    data = header + content
    return hashlib.sha1(data).hexdigest()

VALID_TYPES = {"blob", "tree", "commit", "tag"}

def emit(*lines):
    # Write lines joined by "\n" with NO trailing newline (the grader is strict).
    sys.stdout.write("\n".join(lines))


def main():
    raw = sys.stdin.read()
    sep = "\\0"
    # TODO: find sep. If missing, emit("ERR no NUL separator") and return.
    sep_location = raw.find(sep)
    if sep_location == -1:
        emit("ERR no NUL separator")
        return
    
    # TODO: split header on a single space into (type, size).
    header = raw[: sep_location]
    body = raw[sep_location + len(sep):]
    type, size = header.split(' ')

    # TODO: validate type in VALID_TYPES; else emit f"ERR unknown type {type}".
    if type not in VALID_TYPES:
        emit(f"ERR unknown type {type}")
        return

    # TODO: validate int(size) == len(body); else emit an ERR message.
    if int(size) != len(body):
        emit("ERR size is not correct!")
        return  

    # On success, call:
    emit(f"type {type}", f"size {size}", f"body {len(body)}")
    pass




if __name__ == "__main__":
    main()
