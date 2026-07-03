"""
=========================================================
Gesture Controls
Volume Controller

Author  : Ishant Garg
Version : 2.0.0
Python  : 3.11
=========================================================
"""

from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
from pycaw.pycaw import (
    AudioUtilities,
    IAudioEndpointVolume
)

from src.config import (
    PINCH_MIN_DISTANCE,
    PINCH_MAX_DISTANCE,
    VOLUME_STEP
)


class VolumeController:
    """
    Windows System Volume Controller
    """

    def __init__(self):

        speakers = AudioUtilities.GetSpeakers()

        interface = speakers.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.endpoint = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        self.previous_volume = self.get()

    # --------------------------------------------------

    def get(self):
        """
        Returns volume (0.0 - 1.0)
        """

        return self.endpoint.GetMasterVolumeLevelScalar()

    # --------------------------------------------------

    def get_percentage(self):

        return int(self.get() * 100)

    # --------------------------------------------------

    def set(self, value):
        """
        value -> 0.0 to 1.0
        """

        value = max(0.0, min(1.0, value))

        self.endpoint.SetMasterVolumeLevelScalar(
            value,
            None
        )

    # --------------------------------------------------

    def set_percentage(self, percentage):
        """
        percentage -> 0 to 100
        """

        percentage = max(
            0,
            min(100, percentage)
        )

        self.set(
            percentage / 100
        )

    # --------------------------------------------------

    def increase(self):

        self.set(
            self.get() + VOLUME_STEP
        )

    # --------------------------------------------------

    def decrease(self):

        self.set(
            self.get() - VOLUME_STEP
        )

    # --------------------------------------------------

    def mute(self):

        self.previous_volume = self.get()

        self.set(0.0)

    # --------------------------------------------------

    def unmute(self):

        if self.previous_volume == 0:

            self.previous_volume = 0.50

        self.set(self.previous_volume)

    # --------------------------------------------------

    def toggle_mute(self):

        if self.get() <= 0.01:

            self.unmute()

        else:

            self.mute()

    # --------------------------------------------------

    def set_by_distance(
        self,
        distance
    ):
        """
        Thumb-index distance
        →

        Volume
        """

        distance = max(
            PINCH_MIN_DISTANCE,
            min(
                PINCH_MAX_DISTANCE,
                distance
            )
        )

        volume = (

            distance - PINCH_MIN_DISTANCE

        ) / (

            PINCH_MAX_DISTANCE - PINCH_MIN_DISTANCE

        )

        self.set(volume)

    # --------------------------------------------------

    def info(self):

        return {

            "volume": round(
                self.get(),
                2
            ),

            "percentage": self.get_percentage()

        }
    