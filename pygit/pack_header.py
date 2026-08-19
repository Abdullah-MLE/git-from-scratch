from typing import Iterable, List, Optional, Tuple


PackHeader = Tuple[int, int]


def parse_pack_header(data: bytes) -> Tuple[Optional[PackHeader], Optional[str]]:
    """Validate a packfile header and return its version and object count."""
    if len(data) < 12:
        return None, "ERR truncated"

    if data[:4] != b"PACK":
        return None, "ERR bad magic"

    version = int.from_bytes(data[4:8], "big")
    if version not in {2, 3}:
        return None, f"ERR unsupported version {version}"

    count = int.from_bytes(data[8:12], "big")
    return (version, count), None


def process_pack_headers(lines: Iterable[str]) -> List[str]:
    """Parse hexadecimal pack headers and collect one result per input line."""
    output = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        try:
            data = bytes.fromhex(line)
        except ValueError:
            output.append("ERR bad hex")
            continue

        header, error = parse_pack_header(data)
        if error is not None:
            output.append(error)
            continue

        version, count = header
        output.append(f"PACK v{version} count={count}")

    return output


def run_pack_headers(lines: Iterable[str]) -> str:
    """Process pack headers and return newline-separated output."""
    return "\n".join(process_pack_headers(lines))