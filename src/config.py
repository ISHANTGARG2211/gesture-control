"""
=========================================================
Gesture Controls
Configuration File

Author : Ishant Garg
Version : 1.0.0
Python : 3.11
=========================================================
"""

from pathlib import Path
import cv2

# -------------------------------------------------------
# Project Paths
# -------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = ROOT_DIR / "assets"
MODELS_DIR = ROOT_DIR / "models"
SCREENSHOT_DIR = ROOT_DIR / "screenshots"
TEST_DIR = ROOT_DIR / "tests"

SCREENSHOT_DIR.mkdir(exist_ok=True)

# -------------------------------------------------------
# Camera
# -------------------------------------------------------

CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

WINDOW_TITLE = "Gesture Controls"

# -------------------------------------------------------
# Hand Tracking
# -------------------------------------------------------

MAX_HANDS = 1

DETECTION_CONFIDENCE = 0.75
TRACKING_CONFIDENCE = 0.75

# -------------------------------------------------------
# Gesture Thresholds
# -------------------------------------------------------

PINCH_MIN_DISTANCE = 30
PINCH_MAX_DISTANCE = 220

# -------------------------------------------------------
# Volume
# -------------------------------------------------------

VOLUME_STEP = 0.05

# -------------------------------------------------------
# Cooldown
# -------------------------------------------------------

ACTION_COOLDOWN = 2.0

# -------------------------------------------------------
# URLs
# -------------------------------------------------------

CHATGPT_URL = "https://chatgpt.com"
YOUTUBE_URL = "https://youtube.com"

# -------------------------------------------------------
# Fonts
# -------------------------------------------------------

FONT = cv2.FONT_HERSHEY_SIMPLEX

FONT_SCALE_SMALL = 0.6
FONT_SCALE_MEDIUM = 0.8
FONT_SCALE_LARGE = 1.0

FONT_THICKNESS = 2

# -------------------------------------------------------
# Colors (BGR)
# -------------------------------------------------------

WHITE = (255,255,255)
BLACK = (0,0,0)

GREEN = (0,255,0)
RED = (0,0,255)
BLUE = (255,0,0)

CYAN = (255,255,0)
YELLOW = (0,255,255)
MAGENTA = (255,0,255)

ORANGE = (0,165,255)

GRAY = (160,160,160)

# -------------------------------------------------------
# UI Positions
# -------------------------------------------------------

FPS_POSITION = (20,40)

GESTURE_POSITION = (20,80)

ACTION_POSITION = (20,120)

HAND_POSITION = (20,160)

STATUS_POSITION = (20,690)

# -------------------------------------------------------
# Volume Bar
# -------------------------------------------------------

BAR_LEFT = 50

BAR_TOP = 170

BAR_RIGHT = 90

BAR_BOTTOM = 470

# -------------------------------------------------------
# Gesture Names
# -------------------------------------------------------

PINCH = "PINCH"

FIST = "FIST"

PEACE = "PEACE"

ROCK = "ROCK"

THUMB_UP = "THUMB_UP"

THUMB_DOWN = "THUMB_DOWN"

OPEN_HAND = "OPEN_HAND"

UNKNOWN = "UNKNOWN"

# -------------------------------------------------------
# Keyboard
# -------------------------------------------------------

EXIT_KEY = ord("q")

# -------------------------------------------------------
# Window
# -------------------------------------------------------

WINDOW_MODE = cv2.WINDOW_NORMAL
