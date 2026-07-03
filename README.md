<div align="center">

# ✋ Gesture Controls
### AI Powered Hand Gesture Automation System

Control your computer using only your hand gestures.

Built using **Python, OpenCV, MediaPipe and Pycaw** to provide a real-time touchless interaction system.

---

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge)
![Windows](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge)

</div>

---

# 📚 What I Learned

This project helped me strengthen both my **Artificial Intelligence** and **Software Engineering** skills.

### AI & Computer Vision

- Hand Landmark Detection using MediaPipe
- Real-Time Gesture Recognition
- Human Computer Interaction (HCI)
- Image Processing with OpenCV
- Coordinate Mapping
- Euclidean Distance based Gesture Detection
- Rule-Based AI Gesture Classification
- Real-Time Video Processing

### Software Engineering

- Modular Project Architecture
- Object-Oriented Programming (OOP)
- Logging System
- Exception Handling
- Python Virtual Environment
- Dependency Management
- Clean Code Principles
- Git & GitHub Project Structure

### System Programming

- Windows Audio Control
- Browser Automation
- Screenshot Automation
- Webcam Integration
- File Management

---

# 📖 Overview

Gesture Controls is an AI-powered desktop automation project that allows users to control different computer functions using only hand gestures detected through a webcam.

Instead of relying on traditional input devices like a mouse or keyboard, users interact naturally with their computer using hand gestures.

The project combines **Computer Vision**, **Artificial Intelligence**, and **Automation** to create an intuitive Human Computer Interaction (HCI) experience.

---

# ✨ Features

## 🎵 Volume Control

Control the Windows system volume by changing the distance between your thumb and index finger.

- Smooth volume adjustment
- Real-time volume percentage
- Continuous gesture tracking

---

## 👍 Open ChatGPT

Show a **Thumb Up** gesture to instantly open ChatGPT in your default browser.

---

## ✌ Screenshot Capture

Show the **Peace** gesture to capture your current screen.

Screenshots are automatically saved inside:

```
screenshots/
```

---

## 🤘 Open YouTube

Show the **Rock** gesture to launch YouTube in your default browser.

---

## 📊 Real-Time Information

The application displays:

- FPS
- Current Gesture
- Current Action
- Volume Percentage
- Status
- Hand Detection

---

## 📝 Logging

Application events are automatically saved inside:

```
logs/
```

---

# 🎮 Gesture Mapping

| Gesture | Action |
|----------|--------|
| 🤏 Thumb ↔ Index Distance | Volume Control |
| 👍 Thumb Up | Open ChatGPT |
| ✌ Peace | Take Screenshot |
| 🤘 Rock | Open YouTube |

---

# 🛠 Tech Stack

### Programming Language

- Python 3.11

### Computer Vision

- OpenCV

### AI

- MediaPipe Hands

### Audio

- Pycaw

### Automation

- PyAutoGUI
- WebBrowser

### Utilities

- NumPy
- Comtypes

---

# 📂 Project Structure

```
GESTURE_CONTROLS
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets
│
├── logs
│
├── screenshots
│
├── models
│
├── tests
│
└── src
    │
    ├── __init__.py
    ├── config.py
    ├── camera.py
    ├── hand_tracker.py
    ├── gesture_classifier.py
    ├── volume.py
    ├── action_manager.py
    ├── ui.py
    ├── helpers.py
    └── logger.py
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/GESTURE_CONTROLS.git
```

---

## Navigate to Project

```bash
cd GESTURE_CONTROLS
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

---

## Activate Environment

PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Command Prompt

```cmd
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Project

Run:

```bash
python app.py
```

---

# ▶ Running Again After Closing VS Code

Open VS Code

↓

Open Terminal

↓

Go to Project Folder

```bash
cd path_to_project/GESTURE_CONTROLS
```

Activate Environment

PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Run

```bash
python app.py
```

---

# ⛔ Stop the Application

Press

```
Q
```

or

```
CTRL + C
```

inside the terminal.

---

# 📸 Screenshots

Every screenshot captured using the Peace gesture is automatically saved inside:

```
screenshots/
```

---

# 📝 Logs

Every session creates a log file inside:

```
logs/
```

which contains

- Application Started
- Gestures
- Actions
- Errors
- Shutdown

---

# ⚡ Requirements

- Windows 10/11
- Python 3.11
- Webcam
- Internet Connection (for ChatGPT & YouTube)

---

# 📦 Dependencies

```
opencv-python
mediapipe
numpy
pycaw
comtypes
pyautogui
Pillow
```

---

# 🧠 Working Pipeline

```
Camera
      │
      ▼
OpenCV Frame
      │
      ▼
MediaPipe Hand Detection
      │
      ▼
21 Hand Landmarks
      │
      ▼
Gesture Classification
      │
      ▼
Action Manager
      │
      ▼
Windows Automation
```

---

# 🎯 Future Enhancements

- AI Virtual Mouse
- Gesture Launcher
- Brightness Control
- Media Controller
- Presentation Controller
- Smart Home Control
- Voice Assistant Integration
- Gesture Hub Dashboard
- Deep Learning Gesture Recognition
- Multi-Hand Support

---

# 🤝 How to Experience the Project

1. Launch the application.
2. Stand approximately **40–80 cm** away from the webcam.
3. Ensure your **right hand** is clearly visible.
4. Try the supported gestures:
   - 👍 Thumb Up → Opens ChatGPT
   - ✌ Peace → Captures a Screenshot
   - 🤘 Rock → Opens YouTube
   - 🤏 Move your thumb and index finger closer or farther apart to decrease or increase the system volume.
5. Press **Q** to exit the application.

For the best experience:
- Use a well-lit environment.
- Keep the background simple.
- Avoid covering your fingers.
- Move your hand smoothly for accurate detection.

---

# 👨‍💻 Author

**Ishant Garg**

B.Tech CSE (AI & ML)

JSS Academy of Technical Education, Noida

---

# ⭐ If you like this project

Please consider giving it a **Star ⭐** on GitHub.

It motivates future development and helps others discover the project.

---

<div align="center">

### Made with ❤️ using AI, Computer Vision & Python

</div>