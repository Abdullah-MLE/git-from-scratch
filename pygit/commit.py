from typing import Iterable, List

from .objects import hash_object


def format_identity(identity: str) -> str:
    """Format a lesson identity as a Git author or committer line."""
    name, email, timestamp, timezone = identity.split("|")
    return f"{name} <{email}> {timestamp} {timezone}"


def build_commit_body(
    tree_sha: str,
    parent_shas: Iterable[str],
    author: str,
    committer: str,
    message: str,
) -> str:
    """Build the text body of a Git commit object."""
    lines = [f"tree {tree_sha}"]
    lines.extend(f"parent {sha}" for sha in parent_shas)
    lines.extend([
        f"author {format_identity(author)}",
        f"committer {format_identity(committer)}",
        "",
        message,
    ])
    return "\n".join(lines)


def parse_commit_input(lines: List[str]) -> str:
    """Parse lesson input and return the complete commit body."""
    tree_sha = lines[0]
    parent_count = int(lines[1])
    parent_shas = lines[2:2 + parent_count]
    author = lines[2 + parent_count]
    committer = lines[3 + parent_count]
    message = "\n".join(lines[5 + parent_count:])
    return build_commit_body(tree_sha, parent_shas, author, committer, message)


def hash_commit(body: str) -> str:
    """Hash a commit body as a Git commit object."""
    return hash_object("commit", body)


def run_commit_hash(data: str) -> str:
    """Parse commit input and return its SHA-1 hash."""
    lines = data.split("\n")
    return hash_commit(parse_commit_input(lines)) if lines else ""