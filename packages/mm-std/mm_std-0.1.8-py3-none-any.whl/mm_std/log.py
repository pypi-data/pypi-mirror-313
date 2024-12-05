import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def init_logger(name: str, file_path: str | None = None, file_mkdir: bool = True, level: int = logging.DEBUG) -> logging.Logger:
    log = logging.getLogger(name)
    log.setLevel(level)
    log.propagate = False
    fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(fmt)
    log.addHandler(console_handler)
    if file_path:
        if file_mkdir:
            Path(file_path).parent.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(file_path, maxBytes=10 * 1024 * 1024, backupCount=1)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(fmt)
        log.addHandler(file_handler)
    return log
