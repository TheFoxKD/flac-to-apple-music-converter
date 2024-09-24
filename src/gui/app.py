import tkinter as tk
from pathlib import Path
from threading import Thread
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Optional

from src.core.converter import AudioConverter
from src.core.file_handler import FileHandler
from src.utils.enums import AudioFormat
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class ConverterApp:
    """Main application class for the FLAC to Apple Music Converter."""

    def __init__(self, master: tk.Tk) -> None:
        """Initialize the ConverterApp.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("FLAC to Apple Music Converter")

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.output_format = tk.StringVar(value=AudioFormat.MP3.value)
        self.include_cover_art = tk.BooleanVar(value=True)
        self.progress_var = tk.DoubleVar()

        self.conversion_thread: Optional[Thread] = None
        self.widgets: dict = {}

        self.create_menu()
        self.create_widgets()

    def create_menu(self) -> None:
        """Create the application menu bar."""
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Input Directory", command=self.browse_input)
        file_menu.add_command(
            label="Select Output Directory", command=self.browse_output
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        options_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_checkbutton(
            label="Include Cover Art", variable=self.include_cover_art
        )

        format_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Output Format", menu=format_menu)
        for fmt in AudioFormat:
            format_menu.add_radiobutton(
                label=fmt.value, variable=self.output_format, value=fmt.value
            )

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self) -> None:
        """Create and layout all widgets for the application."""
        self._create_directory_widgets()
        self._create_format_widgets()
        self._create_progress_widgets()
        self._create_convert_button()

    def _create_directory_widgets(self) -> None:
        """Create and layout directory selection widgets."""
        self._create_labeled_entry_with_button(
            "Input Directory:", self.input_dir, self.browse_input, 0
        )
        self._create_labeled_entry_with_button(
            "Output Directory:", self.output_dir, self.browse_output, 1
        )

    def _create_format_widgets(self) -> None:
        """Create and layout format selection and cover art checkbox widgets."""
        self._create_labeled_widget("Output Format:", self._create_format_menu(), 2)
        self.widgets["cover_checkbox"] = ttk.Checkbutton(
            self.master, text="Include cover art", variable=self.include_cover_art
        )
        self.widgets["cover_checkbox"].grid(row=3, column=0, sticky="w")

    def _create_progress_widgets(self) -> None:
        """Create and layout progress bar and label widgets."""
        self.widgets["progress_bar"] = ttk.Progressbar(
            self.master, variable=self.progress_var, maximum=100
        )
        self.widgets["progress_bar"].grid(row=4, column=1, sticky="ew")

        self.widgets["progress_label"] = ttk.Label(self.master, text="")
        self.widgets["progress_label"].grid(row=4, column=2, sticky="w")

    def _create_convert_button(self) -> None:
        """Create and layout the convert button."""
        self.widgets["convert_button"] = ttk.Button(
            self.master, text="Convert", command=self.start_conversion
        )
        self.widgets["convert_button"].grid(row=5, column=1)

    def _create_labeled_entry_with_button(
        self, label_text: str, variable: tk.StringVar, command: Callable, row: int
    ) -> None:
        """Create a labeled entry with a browse button."""
        self._create_labeled_widget(
            label_text, ttk.Entry(self.master, textvariable=variable, width=50), row
        )
        browse_button = ttk.Button(self.master, text="Browse", command=command)
        browse_button.grid(row=row, column=2)
        self.widgets[f'{label_text.lower().replace(" ", "_")}_button'] = browse_button

    def _create_labeled_widget(
        self, label_text: str, widget: tk.Widget, row: int
    ) -> None:
        """Create a labeled widget and add it to the grid."""
        label = ttk.Label(self.master, text=label_text)
        label.grid(row=row, column=0, sticky="w")
        widget.grid(row=row, column=1, sticky="ew")
        self.widgets[label_text.lower().replace(" ", "_")] = widget

    def _create_format_menu(self) -> ttk.OptionMenu:
        """Create the format selection menu."""
        menu = ttk.OptionMenu(
            self.master,
            self.output_format,
            self.output_format.get(),
            *[fmt.value for fmt in AudioFormat],
        )
        self.widgets["format_menu"] = menu
        return menu

    def browse_input(self) -> None:
        """Open a directory dialog to select the input directory."""
        self.input_dir.set(filedialog.askdirectory())

    def browse_output(self) -> None:
        """Open a directory dialog to select the output directory."""
        self.output_dir.set(filedialog.askdirectory())

    def update_progress(self, current: int, total: int) -> None:
        """Update the progress bar and label.

        Args:
            current (int): Current number of processed files.
            total (int): Total number of files to process.
        """
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.widgets["progress_label"].config(text=f"{current}/{total}")

    def start_conversion(self) -> None:
        """Start the conversion process in a separate thread."""
        self._set_interface_state(tk.DISABLED)
        self.conversion_thread = Thread(target=self.convert)
        self.conversion_thread.start()
        self.master.after(100, self.check_conversion_complete)

    def check_conversion_complete(self) -> None:
        """Check if the conversion is complete and update the interface accordingly."""
        if self.conversion_thread and self.conversion_thread.is_alive():
            self.master.after(100, self.check_conversion_complete)
        else:
            self._set_interface_state(tk.NORMAL)
            messagebox.showinfo("Conversion Complete", "All files have been converted.")

    def _set_interface_state(self, state: str) -> None:
        """Set the state of all interactive widgets.

        Args:
            state (str): The state to set (e.g., tk.NORMAL or tk.DISABLED).
        """
        for widget_name, widget in self.widgets.items():
            if isinstance(widget, (ttk.Entry, ttk.Button)):
                widget.config(state=state)
            elif isinstance(widget, ttk.Checkbutton):
                if state == tk.DISABLED:
                    widget.state(["disabled"])
                else:
                    widget.state(["!disabled"])
            elif isinstance(widget, ttk.OptionMenu):
                widget["state"] = state

    def convert(self) -> None:
        """Perform the conversion process."""
        input_path = Path(self.input_dir.get())
        output_path = Path(self.output_dir.get())
        output_format = AudioFormat(self.output_format.get())
        include_cover = self.include_cover_art.get()
        logger.info(
            f"Converting files from {input_path} to {output_format} in {output_path}"
        )

        converter = AudioConverter(
            output_format, num_threads=4, include_cover=include_cover
        )
        file_handler = FileHandler()

        try:
            file_handler.create_output_directory(output_path)
            converted_files = converter.convert_directory(
                input_path,
                output_path,
                progress_callback=self.update_progress_threadsafe,
            )
            logger.info(f"Converted {len(converted_files)} files.")
        except Exception as e:
            logger.error(f"Error during conversion: {str(e)}")
            self.master.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"An error occurred during conversion: {str(e)}"
                ),
            )

        self.master.after(0, self._reset_progress)

    def _reset_progress(self) -> None:
        """Reset the progress bar and label."""
        self.progress_var.set(0)
        self.widgets["progress_label"].config(text="")

    def update_progress_threadsafe(self, current: int, total: int) -> None:
        """Update the progress bar and label in a thread-safe manner.

        Args:
            current (int): Current number of processed files.
            total (int): Total number of files to process.
        """
        self.master.after(0, lambda: self.update_progress(current, total))

    def show_about(self) -> None:
        """Display the About dialog."""
        messagebox.showinfo(
            "About",
            "FLAC to Apple Music Converter\n\n"
            "A simple tool to convert FLAC files to Apple Music compatible formats.\n\n"
            "Version: 1.0\n"
            "Author: Denis (TheFoxKD) Krishtopa\n",
        )
