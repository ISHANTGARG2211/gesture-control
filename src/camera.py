"""
=========================================================
Gesture Controls
Camera Module

Author : Ishant Garg
Version : 2.0.0
=========================================================
"""

import cv2

from src.config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
)


class Camera:
    """
    Camera Manager

    Features
    --------
    ✔ Webcam Initialization
    ✔ Resolution Control
    ✔ Frame Mirroring
    ✔ Camera Information
    ✔ Context Manager Support
    ✔ Safe Cleanup
    """

    def __init__(
        self,
        camera_index=CAMERA_INDEX,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
        mirror=True
    ):

        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.mirror = mirror

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Unable to open camera {self.camera_index}"
            )

        self.set_resolution(width, height)

    # --------------------------------------------------

    def read(self):
        """
        Returns
        -------
        success : bool
        frame   : ndarray
        """

        success, frame = self.cap.read()

        if not success:
            return False, None

        if self.mirror:
            frame = cv2.flip(frame, 1)

        return True, frame

    # --------------------------------------------------

    def set_resolution(self, width, height):

        self.width = width
        self.height = height

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # --------------------------------------------------

    def get_resolution(self):

        width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        return width, height

    # --------------------------------------------------

    def fps(self):

        return self.cap.get(
            cv2.CAP_PROP_FPS
        )

    # --------------------------------------------------

    def opened(self):

        return self.cap.isOpened()

    # --------------------------------------------------

    def release(self):

        if self.opened():
            self.cap.release()

        cv2.destroyAllWindows()

    # --------------------------------------------------

    def __enter__(self):

        return self

    # --------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):

        self.release()
        