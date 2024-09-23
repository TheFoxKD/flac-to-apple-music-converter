# FLAC to Apple Music Compatible Format Converter

This project is a Python-based tool for converting FLAC audio files to formats compatible with Apple Music, such as MP3,
AAC, or ALAC. It provides both a command-line interface and a graphical user interface for ease of use.

## Features

- Convert FLAC files to MP3, AAC, or ALAC formats
- Batch conversion of entire directories
- Graphical user interface for easy file and format selection
- Logging for both audit and diagnostic purposes
- Error handling and reporting

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Prerequisites

This project requires FFmpeg to be installed on your system. You can install it using the following methods:

- On macOS: `brew install ffmpeg`
- On Ubuntu or Debian: `sudo apt-get install ffmpeg`
- On Windows: Download from https://ffmpeg.org/download.html

Make sure FFmpeg is in your system PATH after installation.

## Troubleshooting

If you encounter an error about ffprobe not being found, ensure that FFmpeg is correctly installed and in your system
PATH. You can verify the installation by running `ffmpeg -version` in your terminal.

## Usage

Run the application by executing:

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
- `config/`: Configuration files
- `main.py`: Entry point of the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.