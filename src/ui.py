"""
=========================================================
Gesture Controls
UI Module

Author : Ishant Garg
Version : 1.0.0
=========================================================
"""

import cv2

from src.config import *


class UI:

    def __init__(self):

        self.font = FONT

    # --------------------------------------------------

    def draw_header(self, frame):

        cv2.rectangle(
            frame,
            (0, 0),
            (frame.shape[1], 60),
            (35, 35, 35),
            -1
        )

        cv2.putText(
            frame,
            "GESTURE CONTROLS",
            (20, 40),
            self.font,
            FONT_SCALE_LARGE,
            CYAN,
            FONT_THICKNESS
        )

    # --------------------------------------------------

    def draw_fps(self, frame, fps):

        cv2.putText(
            frame,
            f"FPS : {int(fps)}",
            FPS_POSITION,
            self.font,
            FONT_SCALE_MEDIUM,
            GREEN,
            FONT_THICKNESS
        )

    # --------------------------------------------------

    def draw_hand(self, frame, hand):

        text = "None"

        if hand:
            text = hand

        cv2.putText(
            frame,
            f"Hand : {text}",
            HAND_POSITION,
            self.font,
            FONT_SCALE_MEDIUM,
            CYAN,
            FONT_THICKNESS
        )

    # --------------------------------------------------

    def draw_gesture(self, frame, gesture):

        cv2.putText(
            frame,
            f"Gesture : {gesture}",
            GESTURE_POSITION,
            self.font,
            FONT_SCALE_MEDIUM,
            YELLOW,
            FONT_THICKNESS
        )

    # --------------------------------------------------

    def draw_action(self, frame, action):

        cv2.putText(
            frame,
            f"Action : {action}",
            ACTION_POSITION,
            self.font,
            FONT_SCALE_MEDIUM,
            WHITE,
            FONT_THICKNESS
        )

    # --------------------------------------------------

    def draw_volume(self, frame, percentage):

        percentage = max(0, min(100, percentage))

        fill = int(
            BAR_BOTTOM -
            ((BAR_BOTTOM - BAR_TOP) * percentage / 100)
        )

        cv2.rectangle(
            frame,
            (BAR_LEFT, BAR_TOP),
            (BAR_RIGHT, BAR_BOTTOM),
            WHITE,
            2
        )

        cv2.rectangle(
            frame,
            (BAR_LEFT, fill),
            (BAR_RIGHT, BAR_BOTTOM),
            GREEN,
            -1
        )

        cv2.putText(
            frame,
            f"{percentage} %",
            (BAR_LEFT - 10, BAR_BOTTOM + 35),
            self.font,
            FONT_SCALE_SMALL,
            GREEN,
            2
        )

    # --------------------------------------------------

    def draw_status(self, frame, text):

        cv2.rectangle(

            frame,

            (0, frame.shape[0]-40),

            (frame.shape[1], frame.shape[0]),

            (40,40,40),

            -1

        )

        cv2.putText(

            frame,

            text,

            STATUS_POSITION,

            self.font,

            FONT_SCALE_SMALL,

            ORANGE,

            2

        )

    # --------------------------------------------------

    def draw_landmark(self, frame, landmark):

        cv2.circle(

            frame,

            (landmark.x, landmark.y),

            8,

            MAGENTA,

            -1

        )

    # --------------------------------------------------

    def update(
        self,
        frame,
        fps,
        gesture,
        action,
        hand,
        volume,
        status="Ready"
    ):

        self.draw_header(frame)

        self.draw_fps(frame, fps)

        self.draw_hand(frame, hand)

        self.draw_gesture(frame, gesture)

        self.draw_action(frame, action)

        self.draw_volume(frame, volume)

        self.draw_status(frame, status)

        return frame
    