import tkinter as tk

from src.gui.app import ConverterApp
from src.utils.logging_config import get_logger
from src.utils.startup import check_ffmpeg

logger = get_logger(__name__)


def main():
    root = tk.Tk()
    app = ConverterApp(root)
    logger.info("Application started")
    root.mainloop()
    logger.info("Application closed")


if __name__ == "__main__":
    check_ffmpeg()
    main()
