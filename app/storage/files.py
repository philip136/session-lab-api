from pathlib import Path
from uuid import uuid4


def save_bytes(
    content: bytes,
    directory: str | Path,
    suffix: str,
) -> Path:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    path = directory / f"{uuid4()}{suffix}"
    path.write_bytes(content)

    return path


def remove_file(path: str | Path) -> None:
    Path(path).unlink(missing_ok=True)
