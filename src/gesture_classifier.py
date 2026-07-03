"""
=========================================================
Gesture Controls
Gesture Classifier

Author  : Ishant Garg
Version : 4.0.0
Optimized for Right Hand
=========================================================
"""

from src.config import (
    PEACE,
    ROCK,
    THUMB_UP,
    OPEN_HAND,
    UNKNOWN,
)


class GestureClassifier:
    """
    Detects only static gestures.

    Volume control is NOT handled here.
    Volume is handled directly inside app.py
    using thumb-index distance.
    """

    def __init__(self):

        self.tip_ids = [4, 8, 12, 16, 20]

    # -------------------------------------------------

    def __call__(self, hand):

        return self.classify(hand)

    # -------------------------------------------------

    def finger_states(self, hand):
        """
        Returns finger states.

        Thumb, Index, Middle, Ring, Little

        1 = Up
        0 = Down
        """

        thumb = hand[4].x > hand[3].x

        index = hand[8].y < hand[6].y

        middle = hand[12].y < hand[10].y

        ring = hand[16].y < hand[14].y

        little = hand[20].y < hand[18].y

        return [

            int(thumb),

            int(index),

            int(middle),

            int(ring),

            int(little)

        ]

    # -------------------------------------------------

    def is_thumb_up(self, hand):
        """
        Thumb up with all fingers folded.
        """

        return (

            hand[4].y < hand[3].y < hand[2].y

            and

            hand[8].y > hand[6].y

            and

            hand[12].y > hand[10].y

            and

            hand[16].y > hand[14].y

            and

            hand[20].y > hand[18].y

        )

    # -------------------------------------------------

    def classify(self, hand):

        fingers = self.finger_states(hand)

        # ---------------------------------

        if self.is_thumb_up(hand):

            return THUMB_UP

        # ---------------------------------

        if fingers == [1, 1, 1, 1, 1]:

            return OPEN_HAND

        # ---------------------------------

        if fingers == [0, 1, 1, 0, 0]:

            return PEACE

        # ---------------------------------

        if fingers == [0, 1, 0, 0, 1]:

            return ROCK

        # ---------------------------------

        return UNKNOWN

    # -------------------------------------------------

    def debug(self, hand):

        return {

            "gesture": self.classify(hand),

            "fingers": self.finger_states(hand),

            "thumb_index_distance": round(
                hand.distance(4, 8),
                2
            )

        }
    