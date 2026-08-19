import sys, hashlib
from pygit.objects import hash_object

# Compute the SHA-1 of a tree object built from given entries.
# Tree body entry format: "<mode> <name>\0<20-byte-binary-sha>"
# Entries MUST be sorted by name (byte order).


def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    count = int(lines[0])
    entries = []
    for i in range(1, count + 1):
        parts = lines[i].split(" ")
        mode, name, hex_sha = parts[0], parts[1], parts[2]
        entries.append((mode, name, hex_sha))
    # TODO: sort entries by name.
    entries.sort(key=lambda x: x[1])

    # TODO: build body by concatenating f"{mode} {name}\0" + bytes.fromhex(hex_sha).
    body = b""
    for mode, name, hex_sha in entries:
        body += f"{mode} {name}\0".encode("utf-8") + bytes.fromhex(hex_sha)

    # TODO: wrap with "tree <body_size>\0" header and SHA-1; emit hex digest.

    # Use sys.stdout.write — the grader checks the bytes exactly (no trailing newline).
    sys.stdout.write(hash_object("tree", body))


if __name__ == "__main__":
    main()
