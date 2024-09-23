import subprocess
import sys

from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def check_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error(
            "FFmpeg is not installed or not in PATH. Please install FFmpeg and try again."
        )
        sys.exit(1)
