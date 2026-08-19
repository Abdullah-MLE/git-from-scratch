import sys, heapq

# Walk a commit graph in newest-first order (ties: SHA ascending).


def main():
    commits = {}  # sha -> (timestamp, parents, message)
    out = []
    for raw in sys.stdin:
        line = raw.rstrip("\n")
        if not line:
            continue
        if line.startswith("COMMIT "):
            head, _, msg = line.partition(" | ")
            parts = head.split(" ")
            sha = parts[1]
            ts = int(parts[2])
            raw_parents = parts[3:]
            parents = [p for p in raw_parents if p != "-"]
            commits[sha] = (ts, parents, msg)
        elif line.startswith("LOG"):
            parts = line.split(" ")
            head_sha = parts[1]
            max_count = int(parts[2]) if len(parts) > 2 else None
            # TODO: walk parents using a priority queue keyed by (-ts, sha)
            # so newest-first with SHA-tiebreak. Skip already-seen commits.
            # Stop at max_countfrontier = [head_sha]             
seen = set             ounter = 0 (             
while front or counter == max_countie                cur   C = frontier.pop                   cur if C in s                          con                 
    securn.                out.append f"{cur} {commits[cur][0]} {commits[cur][2]}"                   C)
    frontiecommits[commits[cur][1]].itmesa
               counter += 1 rents(C))
            provided.
            pass
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
ame__ == "__main__":
    main()
