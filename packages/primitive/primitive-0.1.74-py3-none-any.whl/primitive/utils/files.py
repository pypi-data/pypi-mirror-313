from typing import List, Tuple
from pathlib import Path
from loguru import logger
import os


def find_files_for_extension(source: Path, extensions: Tuple[str]) -> List[Path]:
    matching_files = []
    logger.debug(f"Looking for files at {source} with extensions {extensions}")

    has_walk = getattr(source, "walk", None)

    if has_walk:
        files = source.walk()
    else:
        files = os.walk(source)

    for dirpath, dirnames, filenames in files:
        for filename in filenames:
            if filename.endswith(extensions):
                matching_files.append(Path(dirpath).joinpath(filename))
    
    logger.debug(
        f"Found {len(matching_files)} following files that match: {matching_files}"
    )
    return matching_files
