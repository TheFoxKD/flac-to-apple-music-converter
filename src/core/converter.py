from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, List, Optional

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3
from pydub import AudioSegment

from src.utils.enums import AudioFormat
from src.utils.exceptions import ConversionError
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class SingleFileConverter:
    """A class for converting a single FLAC file to another audio format."""

    def __init__(self, output_format: AudioFormat, include_cover: bool):
        self.output_format = output_format
        self.include_cover = include_cover

    def convert(self, input_path: Path, output_path: Path) -> Path:
        """
        Convert a single FLAC file to the specified output format.

        Args:
            input_path (Path): Path to the input FLAC file.
            output_path (Path): Path for the output file.

        Returns:
            Path: Path to the converted file.

        Raises:
            ConversionError: If there's an error during conversion.
        """
        try:
            audio = AudioSegment.from_file(input_path, format="flac")
            audio.export(output_path, format=self.output_format.value)
            self._copy_metadata(input_path, output_path)
            logger.info(f"Converted {input_path} to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error converting {input_path}: {str(e)}")
            raise ConversionError(f"Failed to convert {input_path}: {str(e)}")

    def _copy_metadata(self, src_path: Path, dest_path: Path) -> None:
        """Copy metadata from the source FLAC file to the destination file."""
        src_audio = FLAC(src_path)
        dest_audio = MutagenFile(dest_path, easy=True)
        for tag in src_audio:
            if tag in EasyID3.valid_keys.keys():
                dest_audio[tag] = src_audio[tag]
        dest_audio.save()

        if self.include_cover:
            self._copy_cover_art(src_path, dest_path)

    def _copy_cover_art(self, src_path: Path, dest_path: Path) -> None:
        """Copy cover art from the source FLAC file to the destination file."""
        src_audio = FLAC(src_path)
        dest_audio = ID3(dest_path)
        for picture in src_audio.pictures:
            dest_audio.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime=picture.mime,
                    type=3,  # 3 is for the cover(front) image
                    desc="Cover",
                    data=picture.data,
                )
            )
        dest_audio.save(v2_version=3)


class AudioConverter:
    """A class for converting FLAC files to other audio formats."""

    def __init__(
        self,
        output_format: AudioFormat = AudioFormat.MP3,
        num_threads: int = 4,
        include_cover: bool = True,
    ):
        self.output_format = output_format
        self.num_threads = num_threads
        self.include_cover = include_cover

    def convert_directory(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> List[Path]:
        """
        Convert all FLAC files in a directory to the specified output format using parallel processing.

        Args:
            input_dir (Path): Input directory containing FLAC files.
            output_dir (Optional[Path]): Output directory for converted files.
            progress_callback (Optional[Callable[[int, int], None]]): Callback function to report progress.

        Returns:
            List[Path]: List of paths to converted files.
        """
        flac_files = list(input_dir.glob("**/*.flac"))
        total_files = len(flac_files)
        converted_files = []

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_file = {}
            for flac_file in flac_files:
                output_path = self._get_output_path(flac_file, input_dir, output_dir)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                converter = SingleFileConverter(self.output_format, self.include_cover)
                future = executor.submit(converter.convert, flac_file, output_path)
                future_to_file[future] = flac_file

            for i, future in enumerate(as_completed(future_to_file)):
                flac_file = future_to_file[future]
                try:
                    converted_file = future.result()
                    converted_files.append(converted_file)
                except ConversionError as e:
                    logger.warning(f"Skipping file due to conversion error: {str(e)}")

                if progress_callback:
                    progress_callback(i + 1, total_files)

        return converted_files

    def _get_output_path(
        self, flac_file: Path, input_dir: Path, output_dir: Optional[Path]
    ) -> Path:
        """
        Determine the output path for a converted file.

        Args:
            flac_file (Path): Input FLAC file path.
            input_dir (Path): Input directory path.
            output_dir (Optional[Path]): Output directory path, if specified.

        Returns:
            Path: Output path for the converted file.
        """
        if output_dir:
            relative_path = flac_file.relative_to(input_dir)
            return output_dir / relative_path.with_suffix(
                f".{self.output_format.value}"
            )
        else:
            return flac_file.with_suffix(f".{self.output_format.value}")
