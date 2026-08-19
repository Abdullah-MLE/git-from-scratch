import sys

# Implement `git cat-file` flag dispatcher: -t/-s/-p/-e.


def main():
    store = {}  # sha -> (type, body)
    out = []
    for raw in sys.stdin:
        line = raw.rstrip("\n")
        if not line:
            continue
        if line.startswith("OBJ "):
            parts = line.split(" ", 3)
            sha = parts[1]
            otype = parts[2]
            body = parts[3] if len(parts) > 3 else ""
            # Multi-line bodies use literal "\n" (two chars) — convert to real newline.
            body = body.replace("\\n", "\n")
            store[sha] = (otype, body)
        elif line.startswith("QUERY "):
            parts = line.split(" ", 2)
            flag = parts[1]
            sha = parts[2]
            # TODO: handle each flag
            #   -e -> "ok" if exists else "missing"
            if flag =='-e':
                if sha in store:
                    out.append("ok")
                else:
                    out.append("missing")

            #   -t -> object type (or "fatal: not a valid object name <sha>")
            if flag == '-t':
                if sha in store:
                    out.append(f"{store[sha][0]}")
                else:
                    out.append(f"fatal: not a valid object name {sha}")

            #   -s -> byte length of body (utf-8)
            if flag == '-s':
                if sha in store:
                    out.append(f"{len(store[sha][1])}")
                else:
                    out.append(f"fatal: not a valid object name {sha}")

            #   -p -> body, verbatim
            if flag == '-p':
                if sha in store:
                    out.append(store[sha][1])
                else:
                    out.append(f"fatal: not a valid object name {sha}")
            
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
