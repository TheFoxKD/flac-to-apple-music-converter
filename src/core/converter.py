import logging
from pathlib import Path
from typing import List, Optional

from pydub import AudioSegment

from src.utils.exceptions import ConversionError
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class AudioConverter:
    """
    A class for converting FLAC files to other audio formats.
    """

    def __init__(self, output_format: str = "mp3") -> None:
        self.output_format = output_format
        # Set FFmpeg path
        AudioSegment.converter = "/usr/local/bin/ffmpeg"
        AudioSegment.ffmpeg = "/usr/local/bin/ffmpeg"
        AudioSegment.ffprobe = "/usr/local/bin/ffprobe"

    def convert_file(self, input_path: Path, output_path: Path) -> Path:
        """
        Convert a single FLAC file to the specified output format.

        Args:
            input_path (Path): Path to the input FLAC file.
            output_path (Optional[Path]): Path for the output file. If None, uses the same directory as input.

        Returns:
            Path: Path to the converted file.

        Raises:
            ConversionError: If there's an error during conversion.
        """
        try:
            if output_path is None:
                output_path = input_path.with_suffix(f".{self.output_format}")

            audio = AudioSegment.from_file(input_path, format="flac")
            audio.export(output_path, format=self.output_format)

            logger.info(f"Converted {input_path} to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error converting {input_path}: {str(e)}")
            raise ConversionError(f"Failed to convert {input_path}: {str(e)}")

    def convert_directory(
        self, input_dir: Path, output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Convert all FLAC files in a directory to the specified output format.

        Args:
            input_dir (Path): Path to the input directory containing FLAC files.
            output_dir (Optional[Path]): Path for the output directory. If None, uses the same directory as input.

        Returns:
            List[Path]: List of paths to the converted files.
        """
        converted_files = []
        for flac_file in input_dir.glob("**/*.flac"):
            if output_dir:
                relative_path = flac_file.relative_to(input_dir)
                output_path = output_dir / relative_path.with_suffix(
                    f".{self.output_format}"
                )
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = None

            try:
                converted_file = self.convert_file(flac_file, output_path)
                converted_files.append(converted_file)
            except ConversionError as e:
                logger.warning(f"Skipping file due to conversion error: {str(e)}")

        return converted_files
