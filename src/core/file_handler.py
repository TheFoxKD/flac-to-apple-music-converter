import logging
import shutil
from pathlib import Path
from typing import List

from src.utils.exceptions import FileOperationError
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class FileHandler:
    """
    A class for handling file operations related to audio conversion.
    """

    @staticmethod
    def get_flac_files(directory: Path) -> List[Path]:
        """
        Get all FLAC files in a directory and its subdirectories.

        Args:
            directory (Path): Path to the directory to search.

        Returns:
            List[Path]: List of paths to FLAC files.

        Raises:
            FileOperationError: If there's an error accessing the directory.
        """
        try:
            return list(directory.glob("**/*.flac"))
        except Exception as e:
            logger.error(f"Error accessing directory {directory}: {str(e)}")
            raise FileOperationError(
                f"Failed to access directory {directory}: {str(e)}"
            )

    @staticmethod
    def create_output_directory(output_dir: Path) -> None:
        """
        Create the output directory if it doesn't exist.

        Args:
            output_dir (Path): Path to the output directory.

        Raises:
            FileOperationError: If there's an error creating the directory.
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating output directory {output_dir}: {str(e)}")
            raise FileOperationError(
                f"Failed to create output directory {output_dir}: {str(e)}"
            )

    @staticmethod
    def clean_output_directory(output_dir: Path) -> None:
        """
        Remove all files in the output directory.

        Args:
            output_dir (Path): Path to the output directory.

        Raises:
            FileOperationError: If there's an error cleaning the directory.
        """
        try:
            for item in output_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        except Exception as e:
            logger.error(f"Error cleaning output directory {output_dir}: {str(e)}")
            raise FileOperationError(
                f"Failed to clean output directory {output_dir}: {str(e)}"
            )
