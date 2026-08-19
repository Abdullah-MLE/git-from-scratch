import sys
from typing import Dict, Tuple, List, Optional
from objects import hash_object, get_object_path


class MemoryStore:
    def __init__(self) -> None:
        # Maps sha -> (type, body)
        self._store: Dict[str, Tuple[str, str]] = {}

    def write(self, obj_type: str, body: str) -> str:
        sha = hash_object(obj_type, body)
        self._store[sha] = (obj_type, body)
        return sha

    def read(self, sha: str) -> str:
        if sha not in self._store:
            return "ERR not found"
        obj_type, body = self._store[sha]
        return f"{obj_type} {body}"

    def get_path(self, sha: str) -> str:
        return get_object_path(sha)

    def is_missing(self, sha: str) -> str:
        return "yes" if sha not in self._store else "no"

    def execute_command(self, line: str) -> Optional[str]:
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
        output = []
        for line in lines:
            result = self.execute_command(line)
            if result is not None:
                output.append(result)
        return output


def run_simulator() -> None:
    store = MemoryStore()
    lines = sys.stdin.readlines()
    output = store.process_stream(lines)
    sys.stdout.write("\n".join(output))