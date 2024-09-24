import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from src.core.converter import AudioConverter
from src.core.file_handler import FileHandler
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class ConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("FLAC to Apple Music Converter")

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_format = tk.StringVar(value="mp3")
        self.include_cover_art = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        # Input directory selection
        tk.Label(self.master, text="Input Directory:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.master, textvariable=self.input_dir, width=50).grid(
            row=0, column=1
        )
        tk.Button(self.master, text="Browse", command=self.browse_input).grid(
            row=0, column=2
        )

        # Output directory selection
        tk.Label(self.master, text="Output Directory:").grid(
            row=1, column=0, sticky="w"
        )
        tk.Entry(self.master, textvariable=self.output_dir, width=50).grid(
            row=1, column=1
        )
        tk.Button(self.master, text="Browse", command=self.browse_output).grid(
            row=1, column=2
        )

        # Output format selection
        tk.Label(self.master, text="Output Format:").grid(row=2, column=0, sticky="w")
        tk.OptionMenu(self.master, self.output_format, "mp3", "aac", "alac").grid(
            row=2, column=1, sticky="w"
        )

        # Checkbox for including cover art
        tk.Checkbutton(
            self.master, text="Include cover art", variable=self.include_cover_art
        ).grid(row=3, column=0, sticky="w")

        # Convert button
        tk.Button(self.master, text="Convert", command=self.convert).grid(
            row=4, column=1
        )

    def browse_input(self):
        self.input_dir.set(filedialog.askdirectory())

    def browse_output(self):
        self.output_dir.set(filedialog.askdirectory())

    def convert(self):
        input_path = Path(self.input_dir.get())
        output_path = Path(self.output_dir.get())
        output_format = self.output_format.get()
        include_cover = self.include_cover_art.get()

        converter = AudioConverter(
            output_format, num_threads=4, include_cover=include_cover
        )
        file_handler = FileHandler()

        try:
            file_handler.create_output_directory(output_path)
            converted_files = converter.convert_directory(input_path, output_path)
            logger.info(f"Converted {len(converted_files)} files.")
            tk.messagebox.showinfo(
                "Conversion Complete",
                f"Successfully converted {len(converted_files)} files.",
            )
        except Exception as e:
            logger.error(f"Error during conversion: {str(e)}")
            tk.messagebox.showerror(
                "Error", f"An error occurred during conversion: {str(e)}"
            )
