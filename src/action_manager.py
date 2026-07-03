"""
=========================================================
Gesture Controls
Action Manager

Author : Ishant Garg
Version : 1.0.0
=========================================================
"""

import time
import webbrowser
from datetime import datetime

import pyautogui

from src.config import (
    CHATGPT_URL,
    YOUTUBE_URL,
    SCREENSHOT_DIR,
    ACTION_COOLDOWN
)


class ActionManager:

    def __init__(self):

        self.last_action = 0

    # --------------------------------------------------

    def _ready(self):

        return (
            time.time() - self.last_action
        ) >= ACTION_COOLDOWN

    # --------------------------------------------------

    def _update(self):

        self.last_action = time.time()

    # --------------------------------------------------

    def open_chatgpt(self):

        if not self._ready():
            return "Cooldown"

        webbrowser.open(CHATGPT_URL)

        self._update()

        return "ChatGPT Opened"

    # --------------------------------------------------

    def open_youtube(self):

        if not self._ready():
            return "Cooldown"

        webbrowser.open(YOUTUBE_URL)

        self._update()

        return "YouTube Opened"

    # --------------------------------------------------

    def screenshot(self):

        if not self._ready():
            return "Cooldown"

        filename = datetime.now().strftime(
            "Screenshot_%Y%m%d_%H%M%S.png"
        )

        filepath = SCREENSHOT_DIR / filename

        image = pyautogui.screenshot()

        image.save(filepath)

        self._update()

        return f"Saved : {filename}"

    # --------------------------------------------------

    def custom_url(self, url):

        if not self._ready():
            return "Cooldown"

        webbrowser.open(url)

        self._update()

        return "Browser Opened"

    # --------------------------------------------------

    def wait_time(self):

        remaining = ACTION_COOLDOWN - (
            time.time() - self.last_action
        )

        return max(
            0,
            round(remaining, 1)
        )

    # --------------------------------------------------

    def reset(self):

        self.last_action = 0
        