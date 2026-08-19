import sys, hashlib
from pygit.objects import hash_object

# Build a commit object body in the exact format git uses, then SHA-1.


def main():
    data = sys.stdin.read()
    lines = data.split("\n")
    idx = 0

    tree_sha = lines[idx]; idx += 1

    parent_count = int(lines[idx]); idx += 1
    parents = []
    for _ in range(parent_count):
        parents.append(f"parent {lines[idx]}"); idx += 1
    author_parts = lines[idx].split("|"); idx += 1
    committer_parts = lines[idx].split("|"); idx += 1
    if idx < len(lines) and lines[idx] == "":
        idx += 1
    message = "\n".join(lines[idx:])

    tree_line = f"tree {tree_sha}\n"
    parent_lines = "\n".join(parents) + "\n" if parent_count else  ""
    author_line = f"author {author_parts[0]} <{author_parts[1]}> {author_parts[2]} {author_parts[3]}\n"
    committer_line = f"committer {committer_parts[0]} <{committer_parts[1]}> {committer_parts[2]} {committer_parts[3]}\n"
    blank_line = "\n"

    commit = tree_line + parent_lines + author_line + committer_line + blank_line + message
    
    # TODO: build body lines:
    #   tree <tree_sha>
    #   parent <parent_sha>     (per parent)
    #   author <name> <email-in-angle-brackets> <ts> <tz>
    #   committer ...           (same format)
    #   <blank>
    #   <message>
    # Then wrap with "commit <size>\0" and SHA-1. Emit hex via sys.stdout.write
    # (no trailing newline — the grader compares bytes exactly).
    sys.stdout.write(hash_object("commit", commit))


if __name__ == "__main__":
    main()
