"""Custom default handler and function for logging in a tkinter Text widget."""

from logging import Formatter, Handler
from typing import TYPE_CHECKING

from pgi_logging.utils import LoggerLevel

if TYPE_CHECKING:
    from logging import LogRecord

import tkinter as tk


# Custom Handler class for a tkinter ScrolledText widget
# LINK: https://gist.github.com/bitsgalore/901d0abe4b874b483df3ddc4168754aa
class TkinterTextHandler(Handler):
    """Custom Handler class for a tkinter ScrolledText widget."""

    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text: tk.Text) -> None:
        """Initialize the TkinterTextHandler.

        Args:
        ----
            text (tk.Text): The Text widget to log to.

        """
        # run the regular Handler __init__
        Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record: "LogRecord") -> None:  # noqa
        msg = self.format(record)

        def append() -> None:
            self.text.configure(state="normal")
            self.text.insert(tk.END, msg + "\n")
            self.text.configure(state="disabled")
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


SimpleTkinterFormatter = Formatter(
    fmt="%(levelname)-8s- %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    style="%",
)

VerboseTkinterFormatter = Formatter(
    fmt="[%(asctime)s] %(levelname)-8s- %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    style="%",
)


def get_tkinter_handler(
    text_widget: tk.Text,
    log_level: LoggerLevel = LoggerLevel.DEBUG,
    verbose: bool = False,
) -> TkinterTextHandler:
    """Create a TkinterTextHandler with a custom formatter."""
    if verbose:
        formatter = VerboseTkinterFormatter
    else:
        formatter = SimpleTkinterFormatter

    # Create the handler and set the formatter and the level
    handler = TkinterTextHandler(text_widget)
    handler.setFormatter(formatter)
    handler.setLevel(log_level.value)
    return handler
