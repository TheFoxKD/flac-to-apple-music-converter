# FLAC to Apple Music Compatible Format Converter

This project is a Python-based tool for converting FLAC audio files to formats compatible with Apple Music, such as MP3.
It provides both a command-line interface and a graphical user interface for ease of use.

<p align="center">
   <img width="792" alt="Снимок экрана 2024-10-11 в 20 24 35" src="https://github.com/user-attachments/assets/7276bd36-a889-4e16-97c7-26d9a8a93dd4">
</p>

## Features

- Convert FLAC files to MP3
- Batch conversion of entire directories
- Graphical user interface for easy file and format selection
- Preserve metadata and album artwork during conversion
- Multi-threaded processing for faster conversions
- Comprehensive logging for both audit and diagnostic purposes
- Robust error handling and reporting

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Prerequisites

- Python 3.7+
- FFmpeg

### Installing FFmpeg

This project requires FFmpeg to be installed on your system. You can install it using the following methods:

- On macOS: `brew install ffmpeg`
- On Ubuntu or Debian: `sudo apt-get install ffmpeg`
- On Windows: Download from https://ffmpeg.org/download.html

Make sure FFmpeg is in your system PATH after installation.

## Troubleshooting

If you encounter an error about ffprobe not being found, ensure that FFmpeg is correctly installed and in your system
PATH. You can verify the installation by running `ffmpeg -version` in your terminal.

## Usage

Run the application with the graphical user interface:

```bash
make run
```

or

```bash
python main.py
```

This will launch the graphical user interface. Select your input directory containing FLAC files, choose an output
directory, select the desired output format, and click "Convert" to begin the conversion process.

## Running Tests

To run the tests for this project, you can use the Makefile provided. Ensure you have `make` installed on your system.
Then, execute the following command in the root directory of the project:

```bash
make test
```

This command will discover and run all the tests in the tests directory using the `unittest` framework.

## Project Structure

- `src/`: Contains the main source code
    - `core/`: Core functionality for audio conversion and file handling
    - `utils/`: Utility modules for logging and custom exceptions
    - `gui/`: Graphical user interface implementation
- `tests/`: Unit tests for core functionality
- `main.py`: Entry point of the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
