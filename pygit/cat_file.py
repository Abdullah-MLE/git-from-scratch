from typing import Dict, Iterable, List, Optional, Tuple


Object = Tuple[str, str]


class CatFileStore:
    def __init__(self) -> None:
        """Create an empty store for cat-file commands."""
        self._objects: Dict[str, Object] = {}

    def add_object(self, sha: str, object_type: str, body: str) -> None:
        """Add or replace an object in the in-memory store."""
        self._objects[sha] = (object_type, body)

    def query(self, flag: str, sha: str) -> str:
        """Return the requested cat-file result for an object SHA-1."""
        if flag == "-e":
            return "ok" if sha in self._objects else "missing"

        if sha not in self._objects:
            return f"fatal: not a valid object name {sha}"

        object_type, body = self._objects[sha]
        if flag == "-t":
            return object_type
        if flag == "-s":
            return str(len(body.encode("utf-8")))
        if flag == "-p":
            return body

        return ""

    def execute_command(self, line: str) -> Optional[str]:
        """Parse and execute one OBJ or QUERY command."""
        line = line.rstrip("\n")
        if not line:
            return None

        if line.startswith("OBJ "):
            parts = line.split(" ", 3)
            sha = parts[1]
            object_type = parts[2]
            body = parts[3] if len(parts) > 3 else ""
            self.add_object(sha, object_type, body.replace("\\n", "\n"))
            return None

        if line.startswith("QUERY "):
            _, flag, sha = line.split(" ", 2)
            return self.query(flag, sha)

        return None

    def process_stream(self, lines: Iterable[str]) -> List[str]:
        """Process commands from an iterable and collect query results."""
        output = []
        for line in lines:
            result = self.execute_command(line)
            if result is not None:
                output.append(result)
        return output


def run_cat_file(lines: Iterable[str]) -> str:
    """Run cat-file commands and return their newline-separated output."""
    store = CatFileStore()
    return "\n".join(store.process_stream(lines))
