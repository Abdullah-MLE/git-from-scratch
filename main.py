import sys

# Parse a packfile's 12-byte header and validate it.
# Header layout (big-endian):
#   bytes 0-3:  magic "PACK"
#   bytes 4-7:  version (uint32) — supported: 2 or 3
#   bytes 8-11: object count (uint32)


def main():
    out = []
    for raw in sys.stdin:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            data = bytes.fromhex(line)
        except ValueError:
            out.append("ERR bad hex")
            continue
        # TODO: validate length >= 12, magic == b"PACK", version in {2, 3}.
        # Emit "PACK v<version> count=<count>" on success.
        # Otherwise emit a specific ERR message:
        #   "ERR truncated"
        version = int.from_bytes(data[4:8], "big")
        count = int.from_bytes(data[8:12], "big")
        if len(data) < 12:
            out.append("ERR truncated")

        #   "ERR bad magic"
        elif data[:4] != b"PACK":
            out.append("ERR bad magic")

        #   "ERR unsupported version <v>"
        elif version != 3 and version != 2:
            out.append(f"ERR unsupported version {version}")

        else:
            out.append(f"PACK v{version} count={count}")
        
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
