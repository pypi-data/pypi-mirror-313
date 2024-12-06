from pathlib import Path
import os

__version__ = "0.1.0"


def filtertree(func, src_dir, dest_dir):
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)
    for curr, _, files in os.walk(src_dir):
        current_dir = Path(curr)
        for file in files:
            src_file_path = current_dir / file
            dest_file_path = dest_dir / src_file_path.relative_to(src_dir)
            dest_file_path.parent.mkdir(parents=True, exist_ok=True)
            func(src_file_path, dest_file_path)
