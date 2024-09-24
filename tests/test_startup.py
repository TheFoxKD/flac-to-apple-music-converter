import subprocess
from unittest.mock import patch

import pytest

from src.utils.startup import check_ffmpeg


@pytest.mark.parametrize(
    "mock_run, expected_exit, expected_log",
    [
        (None, False, False),  # FFmpeg installed
        (FileNotFoundError, True, True),  # FFmpeg not installed
        (
            subprocess.CalledProcessError(1, "ffmpeg"),
            True,
            True,
        ),  # FFmpeg command error
    ],
)
def test_check_ffmpeg(mock_run, expected_exit, expected_log):
    """Test check_ffmpeg function with different scenarios."""
    with patch(
        "src.utils.startup.subprocess.run", side_effect=mock_run
    ) as mock_subprocess_run, patch("src.utils.startup.logger") as mock_logger:

        if expected_exit:
            with pytest.raises(SystemExit):
                check_ffmpeg()
        else:
            check_ffmpeg()

        if expected_log:
            mock_logger.error.assert_called_once_with(
                "FFmpeg is not installed or not in PATH. Please install FFmpeg and try again."
            )
        else:
            mock_logger.error.assert_not_called()


def test_ffmpeg_installed():
    """Test when FFmpeg is installed and in PATH."""
    with patch("src.utils.startup.subprocess.run") as mock_run, patch(
        "src.utils.startup.logger"
    ) as mock_logger:
        check_ffmpeg()

        mock_run.assert_called_once_with(
            ["ffmpeg", "-version"], stdout=-3, stderr=-3, check=True
        )
        mock_logger.error.assert_not_called()


def test_ffmpeg_not_installed():
    """Test when FFmpeg is not installed or not in PATH."""
    with patch(
        "src.utils.startup.subprocess.run", side_effect=FileNotFoundError
    ) as mock_run, patch("src.utils.startup.logger") as mock_logger:
        with pytest.raises(SystemExit):
            check_ffmpeg()

        mock_run.assert_called_once_with(
            ["ffmpeg", "-version"], stdout=-3, stderr=-3, check=True
        )
        mock_logger.error.assert_called_once_with(
            "FFmpeg is not installed or not in PATH. Please install FFmpeg and try again."
        )


def test_ffmpeg_command_error():
    """Test when FFmpeg command returns an error."""
    with patch(
        "src.utils.startup.subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "ffmpeg"),
    ) as mock_run, patch("src.utils.startup.logger") as mock_logger:
        with pytest.raises(SystemExit):
            check_ffmpeg()

        mock_run.assert_called_once_with(
            ["ffmpeg", "-version"], stdout=-3, stderr=-3, check=True
        )
        mock_logger.error.assert_called_once_with(
            "FFmpeg is not installed or not in PATH. Please install FFmpeg and try again."
        )
