import os
from typing import Optional
from echolib.common.logger import logger
from pathlib import Path

def read_file(file_path: str) -> Optional[str]:
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File {file_path} does not exist.")
        return None
    try:
        with path.open('r', encoding='utf-8') as file:
            content = file.read()
            logger.debug(f"Read content from {file_path}")
            return content
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        return None

def write_file(file_path: str, content: str) -> bool:
    path = Path(file_path)
    try:
        with path.open('w', encoding='utf-8') as file:
            file.write(content)
            logger.debug(f"Wrote content to {file_path}")
            return True
    except Exception as e:
        logger.error(f"Failed to write to {file_path}: {e}")
        return False
