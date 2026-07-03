"""
=========================================================
Gesture Controls

Author : Ishant Garg
Version : 4.0.0
=========================================================
"""

import time
import cv2

from src.camera import Camera
from src.hand_tracker import HandTracker
from src.gesture_classifier import GestureClassifier
from src.volume import VolumeController
from src.action_manager import ActionManager
from src.ui import UI
from src.helpers import FPSCounter
from src.logger import AppLogger

from src.config import (
    PEACE,
    ROCK,
    THUMB_UP,
    UNKNOWN,
    WINDOW_TITLE,
    WINDOW_MODE,
    EXIT_KEY,
    PINCH_MIN_DISTANCE,
    PINCH_MAX_DISTANCE,
)


# ==========================================================
# Main
# ==========================================================

def main():

    # ------------------------------------------------------
    # Initialize Modules
    # ------------------------------------------------------

    logger = AppLogger()
    logger.startup()

    camera = Camera()

    tracker = HandTracker()

    classifier = GestureClassifier()

    volume = VolumeController()

    actions = ActionManager()

    ui = UI()

    fps_counter = FPSCounter()

    # ------------------------------------------------------
    # Variables
    # ------------------------------------------------------

    gesture = UNKNOWN

    action = "None"

    status = "Running"

    hand_label = "None"

    cooldown = 1.5

    last_action_time = 0

    cv2.namedWindow(

        WINDOW_TITLE,

        WINDOW_MODE

    )

    # ------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------

    while True:

        success, frame = camera.read()

        if not success:
            break

        fps = fps_counter.update()

        hands = tracker.detect(frame)

        current_time = time.time()

        # --------------------------------------------------
        # Hand Found
        # --------------------------------------------------

        if hands:

            hand = hands[0]

            hand_label = hand.label

            gesture = classifier(hand)

            logger.gesture(gesture)

            # --------------------------------------------------
            # Thumb and Index
            # --------------------------------------------------

            thumb = hand[4]

            index = hand[8]

            cx = (thumb.x + index.x) // 2

            cy = (thumb.y + index.y) // 2

            distance = hand.distance(4, 8)

            # --------------------------------------------------
            # Draw Volume Controller
            # --------------------------------------------------

            cv2.circle(
                frame,
                (thumb.x, thumb.y),
                12,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.circle(
                frame,
                (index.x, index.y),
                12,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.line(
                frame,
                (thumb.x, thumb.y),
                (index.x, index.y),
                (0, 255, 0),
                3
            )

            cv2.circle(
                frame,
                (cx, cy),
                10,
                (0, 255, 0),
                cv2.FILLED
            )

            # --------------------------------------------------
            # Smooth Volume Control
            # --------------------------------------------------

            distance = max(
                PINCH_MIN_DISTANCE,
                min(
                    PINCH_MAX_DISTANCE,
                    distance
                )
            )

            volume.set_by_distance(distance)

            status = f"Volume : {volume.get_percentage()}%"
                        # --------------------------------------------------
            # Gesture Actions
            # --------------------------------------------------

            if current_time - last_action_time > cooldown:

                # ----------------------------------------------
                # Thumb Up → Open ChatGPT
                # ----------------------------------------------

                if gesture == THUMB_UP:

                    action = actions.open_chatgpt()

                    logger.action(action)

                    status = action

                    last_action_time = current_time

                # ----------------------------------------------
                # Peace → Screenshot
                # ----------------------------------------------

                elif gesture == PEACE:

                    action = actions.screenshot()

                    logger.action(action)

                    status = action

                    last_action_time = current_time

                # ----------------------------------------------
                # Rock → Open YouTube
                # ----------------------------------------------

                elif gesture == ROCK:

                    action = actions.open_youtube()

                    logger.action(action)

                    status = action

                    last_action_time = current_time

                else:

                    action = "Volume Control"

        # --------------------------------------------------
        # No Hand Detected
        # --------------------------------------------------

        else:

            gesture = UNKNOWN

            action = "Waiting..."

            hand_label = "None"

            status = "Show Right Hand"

        # --------------------------------------------------
        # Volume Percentage
        # --------------------------------------------------

        volume_percentage = volume.get_percentage()

        # --------------------------------------------------
        # Draw Volume Text
        # --------------------------------------------------

        cv2.putText(

            frame,

            f"Volume : {volume_percentage}%",

            (40, 60),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 0),

            2

        )

        # --------------------------------------------------
        # FPS
        # --------------------------------------------------

        cv2.putText(

            frame,

            f"FPS : {int(fps)}",

            (40, 95),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 0),

            2

        )
                # --------------------------------------------------
        # Draw Gesture
        # --------------------------------------------------

        cv2.putText(

            frame,

            f"Gesture : {gesture}",

            (40, 130),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0, 255, 255),

            2

        )

        # --------------------------------------------------
        # Draw Action
        # --------------------------------------------------

        cv2.putText(

            frame,

            f"Action : {action}",

            (40, 165),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        # --------------------------------------------------
        # Draw Hand
        # --------------------------------------------------

        cv2.putText(

            frame,

            f"Hand : {hand_label}",

            (40, 200),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 0),

            2

        )

        # --------------------------------------------------
        # Draw Status
        # --------------------------------------------------

        cv2.putText(

            frame,

            status,

            (40, 235),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0, 255, 0),

            2

        )

        # --------------------------------------------------
        # Draw Instructions
        # --------------------------------------------------

        cv2.putText(

            frame,

            "Thumb + Index : Volume",

            (40, 640),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2

        )

        cv2.putText(

            frame,

            "Thumb Up : ChatGPT",

            (40, 665),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2

        )

        cv2.putText(

            frame,

            "Peace : Screenshot",

            (40, 690),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2

        )

        cv2.putText(

            frame,

            "Rock : YouTube",

            (40, 715),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2

        )

        # --------------------------------------------------
        # UI Module
        # --------------------------------------------------

        frame = ui.update(

            frame=frame,

            fps=fps,

            gesture=gesture,

            action=action,

            hand=hand_label,

            volume=volume_percentage,

            status=status

        )

        # --------------------------------------------------
        # Display Window
        # --------------------------------------------------

        cv2.imshow(

            WINDOW_TITLE,

            frame

        )

        # --------------------------------------------------
        # Exit Key
        # --------------------------------------------------

        key = cv2.waitKey(1) & 0xFF

        if key == EXIT_KEY:

            break
            # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    logger.info("Closing Gesture Controls...")

    logger.shutdown()

    try:
        tracker.close()
    except Exception:
        pass

    try:
        camera.release()
    except Exception:
        pass

    cv2.destroyAllWindows()

    logger.info("Application Closed Successfully")


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nApplication Stopped By User")

    except Exception as e:

        print(f"\nUnexpected Error : {e}")
        