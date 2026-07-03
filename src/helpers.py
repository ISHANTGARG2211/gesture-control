"""
=========================================================
Gesture Controls
Helper Utilities

Author : Ishant Garg
Version : 1.0.0
=========================================================
"""

import time

import cv2
import numpy as np


# =========================================================
# FPS Counter
# =========================================================

class FPSCounter:

    def __init__(self):

        self.previous_time = time.time()

        self.current_time = time.time()

        self.fps = 0

    # --------------------------------------------------

    def update(self):

        self.current_time = time.time()

        difference = self.current_time - self.previous_time

        if difference != 0:

            self.fps = 1 / difference

        self.previous_time = self.current_time

        return self.fps


# =========================================================
# Distance Mapper
# =========================================================

class DistanceMapper:

    @staticmethod
    def map(
        value,
        in_min,
        in_max,
        out_min,
        out_max
    ):

        value = max(
            in_min,
            min(
                in_max,
                value
            )
        )

        return np.interp(

            value,

            [in_min, in_max],

            [out_min, out_max]

        )


# =========================================================
# Gesture History
# =========================================================

class GestureHistory:

    def __init__(self):

        self.previous = None

        self.current = None

    # --------------------------------------------------

    def update(self, gesture):

        self.previous = self.current

        self.current = gesture

    # --------------------------------------------------

    def changed(self):

        return self.previous != self.current

    # --------------------------------------------------

    def reset(self):

        self.previous = None

        self.current = None


# =========================================================
# Landmark Drawer
# =========================================================

class LandmarkDrawer:

    @staticmethod
    def draw(frame, landmark):

        cv2.circle(

            frame,

            (landmark.x, landmark.y),

            8,

            (255, 0, 255),

            -1

        )

    # --------------------------------------------------

    @staticmethod
    def connect(frame, p1, p2):

        cv2.line(

            frame,

            (p1.x, p1.y),

            (p2.x, p2.y),

            (255,255,255),

            2

        )


# =========================================================
# Timer
# =========================================================

class Timer:

    def __init__(self):

        self.start = time.time()

    # --------------------------------------------------

    def reset(self):

        self.start = time.time()

    # --------------------------------------------------

    def elapsed(self):

        return time.time() - self.start


# =========================================================
# Text Drawer
# =========================================================

class Text:

    @staticmethod
    def draw(
        frame,
        text,
        position,
        font,
        scale,
        color,
        thickness=2
    ):

        cv2.putText(

            frame,

            str(text),

            position,

            font,

            scale,

            color,

            thickness

        )
        