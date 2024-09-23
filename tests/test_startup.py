import subprocess
import unittest
from unittest.mock import MagicMock, patch

from src.utils.startup import check_ffmpeg


class TestCheckFFmpeg(unittest.TestCase):
    @patch("src.utils.startup.subprocess.run")
    @patch("src.utils.startup.logger")
    def test_ffmpeg_installed(
        self, mock_logger: MagicMock, mock_run: MagicMock
    ) -> None:
        """Test when FFmpeg is installed and in PATH."""
        mock_run.return_value = None
        try:
            check_ffmpeg()
        except SystemExit:
            self.fail("check_ffmpeg() raised SystemExit unexpectedly!")
        mock_logger.error.assert_not_called()

    @patch("src.utils.startup.subprocess.run", side_effect=FileNotFoundError)
    @patch("src.utils.startup.logger")
    def test_ffmpeg_not_installed(
        self, mock_logger: MagicMock, mock_run: MagicMock
    ) -> None:
        """Test when FFmpeg is not installed or not in PATH."""
        with self.assertRaises(SystemExit):
            check_ffmpeg()
        mock_logger.error.assert_called_once_with(
            "FFmpeg is not installed or not in PATH. Please install FFmpeg and try again."
        )

    @patch(
        "src.utils.startup.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "ffmpeg"),
    )
    @patch("src.utils.startup.logger")
    def test_ffmpeg_command_error(
        self, mock_logger: MagicMock, mock_run: MagicMock
    ) -> None:
        """Test when FFmpeg command returns an error."""
        with self.assertRaises(SystemExit):
            check_ffmpeg()
        mock_logger.error.assert_called_once_with(
            "FFmpeg is not installed or not in PATH. Please install FFmpeg and try again."
        )


if __name__ == "__main__":
    unittest.main()
