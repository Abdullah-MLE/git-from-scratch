import sys, hashlib
from objects import hash_blob

# Simulate git's loose-object store in memory.


def main():
    store = {}  # sha -> (type, body)
    out = []   # build up output; emit with "\n".join(out) at end (no trailing newline)
    for raw in sys.stdin:
        line = raw.rstrip("\n")
        if not line:
            continue
        parts = line.split(" ", 2)
        cmd = parts[0]
        if cmd == "WRITE":
            otype = parts[1]
            body = parts[2] if len(parts) > 2 else ""
            # TODO: build inflated bytes "otype <len>\0body", SHA-1, store, append sha to out.
            sha1 = hash_blob(body)
            store[sha1] = body
            out.append(sha1)
            
        elif cmd == "READ":
            sha = parts[1]
            # TODO: look up and append "<type> <body>" or "ERR not found".
            if sha not in store:
                out.append("ERR not found")
            else:
                out.append(f"{otype} {store[sha]}")
            
        elif cmd == "PATH":
            sha = parts[1]
            # TODO: append ".git/objects/<first2>/<remaining38>".
            out.append(f".git/objects/{sha[:2]}/{sha[2:]}")
            
        elif cmd == "MISSING":
            sha = parts[1]
            # TODO: append "yes" or "no".
            if sha not in store:
                out.append("no")
            else:
                out.append("yes")            
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
