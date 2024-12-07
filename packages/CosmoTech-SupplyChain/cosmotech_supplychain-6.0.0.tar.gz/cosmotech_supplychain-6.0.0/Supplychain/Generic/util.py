from pathlib import Path
from shutil import rmtree


def clear_directory(directory_path: str):
    """Empty the specified directory (remove all files and directories)."""
    dir_path = Path(directory_path)
    if dir_path.exists() and dir_path.is_dir():
        for item in dir_path.iterdir():
            if item.is_dir():
                rmtree(item)
            else:
                item.unlink()


def str_to_bool(value: str) -> bool:
    value = value.strip().lower()
    if value in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    if value in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    raise ValueError(f"invalid truth value {value!r}")
