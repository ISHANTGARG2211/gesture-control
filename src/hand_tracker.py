"""
=========================================================
Gesture Controls
Hand Tracking Module

Author : Ishant Garg
Version : 2.0.0
Python : 3.11
=========================================================
"""

from dataclasses import dataclass
from typing import List
import math

import cv2
import mediapipe as mp

from src.config import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE,
)


# =========================================================
# Landmark
# =========================================================

@dataclass(slots=True)
class Landmark:
    """
    Represents a single MediaPipe landmark.
    """

    id: int
    x: int
    y: int


# =========================================================
# Hand
# =========================================================

class Hand:
    """
    Represents one detected hand.
    """

    def __init__(self, landmarks: List[Landmark], handedness: str):

        self.landmarks = landmarks
        self.handedness = handedness

    # --------------------------------------------------

    @property
    def label(self):
        """
        Returns:
            Left / Right
        """
        return self.handedness

    # --------------------------------------------------

    def get(self, index: int):

        return self.landmarks[index]

    # --------------------------------------------------

    def distance(self, id1: int, id2: int):

        p1 = self[id1]
        p2 = self[id2]

        return math.hypot(
            p2.x - p1.x,
            p2.y - p1.y
        )

    # --------------------------------------------------

    def center(self):

        x = sum(point.x for point in self.landmarks) // len(self.landmarks)

        y = sum(point.y for point in self.landmarks) // len(self.landmarks)

        return x, y

    # --------------------------------------------------

    def bounding_box(self):

        xs = [p.x for p in self.landmarks]
        ys = [p.y for p in self.landmarks]

        return (
            min(xs),
            min(ys),
            max(xs),
            max(ys)
        )

    # --------------------------------------------------

    def as_list(self):

        return self.landmarks

    # --------------------------------------------------

    def __getitem__(self, index):

        return self.landmarks[index]

    # --------------------------------------------------

    def __len__(self):

        return len(self.landmarks)

    # --------------------------------------------------

    def __iter__(self):

        return iter(self.landmarks)

    # --------------------------------------------------

    def __repr__(self):

        return (
            f"Hand("
            f"label='{self.label}', "
            f"landmarks={len(self.landmarks)})"
        )


# =========================================================
# Hand Tracker
# =========================================================

class HandTracker:
    """
    Detects hands using MediaPipe.
    """

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.mp_draw = mp.solutions.drawing_utils

        self.detector = self.mp_hands.Hands(

            static_image_mode=False,

            max_num_hands=MAX_HANDS,

            min_detection_confidence=DETECTION_CONFIDENCE,

            min_tracking_confidence=TRACKING_CONFIDENCE

        )

    # --------------------------------------------------

    def process(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        rgb.flags.writeable = False

        results = self.detector.process(rgb)

        rgb.flags.writeable = True

        return results

    # --------------------------------------------------

    def detect(
        self,
        frame,
        draw=True
    ) -> List[Hand]:

        results = self.process(frame)

        hands = []

        if not results.multi_hand_landmarks:

            return hands

        h, w = frame.shape[:2]

        for hand_landmarks, handedness in zip(

                results.multi_hand_landmarks,

                results.multi_handedness):

            if draw:

                self.mp_draw.draw_landmarks(

                    frame,

                    hand_landmarks,

                    self.mp_hands.HAND_CONNECTIONS

                )

            points = []

            for idx, landmark in enumerate(hand_landmarks.landmark):

                points.append(

                    Landmark(

                        idx,

                        int(landmark.x * w),

                        int(landmark.y * h)

                    )

                )

            hands.append(

                Hand(

                    points,

                    handedness.classification[0].label

                )

            )

        return hands

    # --------------------------------------------------

    def close(self):

        self.detector.close()
        