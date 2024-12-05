from pathlib import Path


def read_text(path: str | Path) -> str:
    if isinstance(path, str):
        path = Path(path)
    return path.read_text()


def get_filename_without_extension(path: str | Path) -> str:
    if isinstance(path, str):
        path = Path(path)
    return path.stem
