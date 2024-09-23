from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from pydub import AudioSegment

from src.utils.exceptions import ConversionError
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class AudioConverter:
    """
    A class for converting FLAC files to other audio formats.
    """

    def __init__(self, output_format: str = "mp3", num_threads: int = 4):
        self.output_format = output_format
        self.num_threads = num_threads

    def _copy_metadata(self, src_path: Path, dest_path: Path) -> None:
        """
        Copy metadata from the source FLAC file to the destination file.
        """
        src_audio = FLAC(src_path)
        dest_audio = MutagenFile(dest_path, easy=True)

        for tag in src_audio:
            if tag in EasyID3.valid_keys.keys():
                dest_audio[tag] = src_audio[tag]

        dest_audio.save()

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

            self._copy_metadata(input_path, output_path)

            logger.info(f"Converted {input_path} to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error converting {input_path}: {str(e)}")
            raise ConversionError(f"Failed to convert {input_path}: {str(e)}")

    def convert_directory(
        self, input_dir: Path, output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Convert all FLAC files in a directory to the specified output format using parallel processing.
        """
        flac_files = list(input_dir.glob("**/*.flac"))
        converted_files = []

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_file = {}
            for flac_file in flac_files:
                if output_dir:
                    relative_path = flac_file.relative_to(input_dir)
                    output_path = output_dir / relative_path.with_suffix(
                        f".{self.output_format}"
                    )
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    output_path = None

                future = executor.submit(self.convert_file, flac_file, output_path)
                future_to_file[future] = flac_file

            for future in as_completed(future_to_file):
                flac_file = future_to_file[future]
                try:
                    converted_file = future.result()
                    converted_files.append(converted_file)
                except ConversionError as e:
                    logger.warning(f"Skipping file due to conversion error: {str(e)}")

        return converted_files
