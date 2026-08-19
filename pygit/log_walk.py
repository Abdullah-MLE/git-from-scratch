import heapq
from typing import Dict, Iterable, List, Optional, Tuple


Commit = Tuple[int, List[str], str]


def parse_commit_line(line: str) -> Tuple[str, Commit]:
    """Parse one COMMIT line into a SHA and commit data."""
    header, separator, message = line.partition(" | ")
    if not separator:
        message = ""
    parts = header.split()
    sha, timestamp = parts[1], int(parts[2])
    parents = [parent for parent in parts[3:] if parent != "-"]
    return sha, (timestamp, parents, message)


def add_commit(commits: Dict[str, Commit], line: str) -> None:
    """Parse one commit line and add it to the commit map."""
    sha, commit = parse_commit_line(line)
    commits[sha] = commit


def push_commit(frontier: List[Tuple[int, str]], sha: str, commits: Dict[str, Commit]) -> None:
    """Add a commit to the queue using newest-first ordering."""
    timestamp = commits[sha][0]
    # heapq returns the smallest item, so -timestamp puts newer commits first.
    heapq.heappush(frontier, (-timestamp, sha))


def walk_commits(
    commits: Dict[str, Commit], head_sha: str, max_count: Optional[int]
) -> List[str]:
    """Walk reachable commits in newest-first order."""
    frontier: List[Tuple[int, str]] = []
    seen = set()
    output = []
    push_commit(frontier, head_sha, commits)
    while frontier and (max_count is None or len(output) < max_count):
        _, sha = heapq.heappop(frontier)
        if sha in seen:
            continue
        seen.add(sha)
        timestamp, parents, message = commits[sha]
        output.append(f"{sha} {timestamp} {message}")
        for parent in parents:
            push_commit(frontier, parent, commits)
    return output


def process_log_lines(lines: Iterable[str]) -> List[str]:
    """Read commit and log commands and return their output lines."""
    commits: Dict[str, Commit] = {}
    output = []
    for raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("COMMIT "):
            add_commit(commits, line)
        elif line.startswith("LOG "):
            parts = line.split()
            limit = int(parts[2]) if len(parts) > 2 else None
            output.extend(walk_commits(commits, parts[1], limit))
    return output


def run_log_walk(lines: Iterable[str]) -> str:
    """Run log commands and return newline-separated output."""
    return "\n".join(process_log_lines(lines))