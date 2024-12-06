"""Test the pgi_logging module with a tkinter GUI.

Using gist from: https://gist.github.com/bitsgalore/901d0abe4b874b483df3ddc4168754aa
"""

import logging
import threading
import time
import tkinter as tk
import tkinter.scrolledtext as ScrolledText  # type: ignore # noqa

from pgi_logging import pgi_handlers


class GUI(tk.Frame):
    """Class that defines the graphical user interface."""

    # This class defines the graphical user interface
    def __init__(
        self,
        parent: tk.Tk,
        *args,  # noqa
        **kwargs,  # noqa
    ) -> None:
        """Initialize the GUI.

        Args:
        ----
            parent (tk.Tk): The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self._build_gui()

    def _build_gui(self) -> None:
        # Build GUI
        self.root.title("TEST")
        self.root.option_add("*tearOff", "FALSE")
        self.grid(column=0, row=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=1, uniform="a")
        self.grid_columnconfigure(2, weight=1, uniform="a")
        self.grid_columnconfigure(3, weight=1, uniform="a")

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state="disabled")
        st.configure(font="TkFixedFont")
        st.grid(column=0, row=1, sticky="w", columnspan=4)

        # Add a stop button
        stop_button = tk.Button(self, text="Stop", command=self.root.destroy)
        stop_button.grid(column=0, row=2, sticky="w")

        # Create the handlers
        text_handler = pgi_handlers.get_tkinter_handler(
            text_widget=st, verbose=True
        )
        stream_handler = pgi_handlers.get_stream_handler(verbose=True)

        # Initialize the logger with the name 'tkinter'
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(text_handler)
        logger.addHandler(stream_handler)


def worker(stop_event: threading.Event) -> None:
    """Worker function that logs the time every 2 seconds.

    Args:
    ----
        stop_event (threading.Event): Event that signals the worker to stop.

    """
    # Skeleton worker function, runs in separate thread (see below)
    while not stop_event.is_set():
        # Report time / date at 2-second intervals
        time.sleep(2)
        time_str = time.asctime()
        msg = "Current time: " + time_str
        logging.info(msg)


def main() -> None:
    """Main function that initializes the GUI and starts the worker thread."""  # noqa
    # Initialize the GUI
    root = tk.Tk()
    GUI(root)

    # Create a thread for the worker function that logs the time
    t1_stop_event = threading.Event()
    t1 = threading.Thread(target=worker, args=[t1_stop_event], daemon=True)
    t1.start()

    # Start the GUI
    root.mainloop()

    # When the GUI ends, stop the worker thread
    t1_stop_event.set()


if __name__ == "__main__":
    main()
