"""
Terminal spinner used while the assistant is waiting on the model response.
"""

from __future__ import annotations

import itertools
import sys
import threading
import time


class Spinner:
    """
    A simple terminal spinner that runs in a background thread.
    """

    def __init__(self, message: str = "Thinking") -> None:
        self.message = message
        self.frames = itertools.cycle(
            ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        )
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def _spin(self) -> None:
        """
        Render the spinner until told to stop.
        """
        while not self._stop_event.is_set():
            frame = next(self.frames)
            sys.stdout.write(f"\r{frame} {self.message}...")
            sys.stdout.flush()
            time.sleep(0.1)

        # Clear the current line fully
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

    def start(self) -> None:
        """
        Start the spinner thread.
        """
        if self._thread is not None and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the spinner thread and wait for it to finish.
        """
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None
