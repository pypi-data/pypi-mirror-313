from pathlib import Path


def is_local_path(path: str):
    return Path(path).exists()
