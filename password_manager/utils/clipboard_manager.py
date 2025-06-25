"""
Clipboard management utility
"""
import pyperclip
import threading
import time
from ..config.settings import Settings


class ClipboardManager:
    def __init__(self):
        self.settings = Settings()
        self.timeout = self.settings.get("clipboard_timeout", 30)
        self._clear_timer = None

    def copy_to_clipboard(self, text):
        """
        Copy text to clipboard and schedule its clearing
        """
        pyperclip.copy(text)
        self._schedule_clear()

    def _schedule_clear(self):
        """
        Schedule clipboard clearing after timeout
        """
        if self._clear_timer and self._clear_timer.is_alive():
            self._clear_timer.cancel()

        def clear_clipboard():
            pyperclip.copy('')

        self._clear_timer = threading.Timer(self.timeout, clear_clipboard)
        self._clear_timer.daemon = True
        self._clear_timer.start()
