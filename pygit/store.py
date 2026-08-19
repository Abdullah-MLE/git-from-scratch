import sys
from typing import Dict, List, Optional, Tuple
from .objects import hash_object, get_object_path


class MemoryStore:
    def __init__(self) -> None:
        """Create an empty in-memory object store."""
        # Maps sha -> (type, body)
        self._store: Dict[str, Tuple[str, str]] = {}

    def write(self, obj_type: str, body: str) -> str:
        """Hash an object, store it, and return its SHA-1."""
        sha = hash_object(obj_type, body)
        self._store[sha] = (obj_type, body)
        return sha

    def read(self, sha: str) -> str:
        """Return a stored object's type and body, or a missing error."""
        if sha not in self._store:
            return "ERR not found"
        obj_type, body = self._store[sha]
        return f"{obj_type} {body}"

    def get_path(self, sha: str) -> str:
        """Return the loose-object path for a stored object's SHA-1."""
        return get_object_path(sha)

    def is_missing(self, sha: str) -> str:
        """Report whether an object is absent from the store."""
        return "yes" if sha not in self._store else "no"

    def execute_command(self, line: str) -> Optional[str]:
        """Execute one simulator command and return its output."""
        line = line.rstrip("\n")
        if not line:
            return None

        parts = line.split(" ", 2)
        cmd = parts[0]

        if cmd == "WRITE":
            obj_type = parts[1]
            body = parts[2] if len(parts) > 2 else ""
            return self.write(obj_type, body)

        if cmd == "READ":
            sha = parts[1]
            return self.read(sha)

        if cmd == "PATH":
            sha = parts[1]
            return self.get_path(sha)

        if cmd == "MISSING":
            sha = parts[1]
            return self.is_missing(sha)

        return None

    def process_stream(self, lines: List[str]) -> List[str]:
        """Execute simulator commands and collect their outputs."""
        output = []
        for line in lines:
            result = self.execute_command(line)
            if result is not None:
                output.append(result)
        return output


def run_simulator() -> None:
    """Run the memory-store simulator using standard input and output."""
    store = MemoryStore()
    lines = sys.stdin.readlines()
    output = store.process_stream(lines)
    sys.stdout.write("\n".join(output))