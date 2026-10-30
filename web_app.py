"""
=========================================================
Gesture Controls
FastAPI Control Dashboard Server

Author : Antigravity & Ishant Garg
Version : 1.0.0
=========================================================
"""

import os
import cv2
import time
import json
import queue
import logging
import threading
import asyncio
import webbrowser
import subprocess
from pathlib import Path
from typing import Generator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.camera import Camera
from src.hand_tracker import HandTracker
from src.gesture_classifier import GestureClassifier
from src.volume import VolumeController
from src.action_manager import ActionManager
from src.ui import UI
from src.helpers import FPSCounter
from src.logger import AppLogger
import src.config as config

# Setup FastAPI App
app = FastAPI(title="Gesture Controls Dashboard", version="1.0.0")

# Setup custom logging queue handler to stream real-time events to the UI
log_queue = queue.Queue(maxsize=200)

class WebLogHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)
            log_queue.put_nowait(log_entry)
        except queue.Full:
            try:
                # Remove oldest log line and add the new one
                log_queue.get_nowait()
                log_queue.put_nowait(log_entry)
            except Exception:
                pass
        except Exception:
            pass

# Attach our custom handler to the gesture control logger
logger = logging.getLogger("GestureControls")
web_handler = WebLogHandler()
web_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
web_handler.setFormatter(web_formatter)
web_handler.setLevel(logging.INFO)
logger.addHandler(web_handler)


# ==========================================================
# GESTURE ENGINE THREAD MANAGEMENT
# ==========================================================

# Thread-safe queue for OS-level actions (webbrowser, screenshot)
_action_queue = queue.Queue(maxsize=10)

def _open_url(url: str):
    """Open a URL using Windows shell start command — works from any process context."""
    subprocess.Popen(f'start "" "{url}"', shell=True)

def _action_executor_thread():
    """Runs in a dedicated thread to safely execute OS-level actions."""
    while True:
        try:
            action_name, action_fn = _action_queue.get(timeout=1)
            try:
                action_fn()
            except Exception as e:
                logging.getLogger("GestureControls").error(f"Action '{action_name}' failed: {e}")
            finally:
                _action_queue.task_done()
        except queue.Empty:
            continue

# Start the executor thread once at module load
_executor = threading.Thread(target=_action_executor_thread, daemon=True)
_executor.start()


class GestureEngine:
    def __init__(self):
        self.active = False
        self.thread = None
        self.latest_jpeg = None
        self.fps = 0.0
        self.hand_label = "None"
        self.gesture = "UNKNOWN"
        self.action = "None"
        self.volume_percentage = 0
        self.status = "Stopped"
        self.lock = threading.Lock()
        
    def start(self):
        with self.lock:
            if not self.active:
                self.active = True
                self.status = "Starting..."
                self.thread = threading.Thread(target=self._run_loop, daemon=True)
                self.thread.start()
                
    def stop(self):
        with self.lock:
            if self.active:
                self.active = False
                self.status = "Stopping..."
                
    def _run_loop(self):
        app_logger = AppLogger()
        app_logger.startup()
        
        camera = None
        tracker = None
        classifier = None
        volume = None
        actions = None
        ui = None
        fps_counter = None
        
        try:
            camera = Camera(camera_index=config.CAMERA_INDEX)
            tracker = HandTracker()
            classifier = GestureClassifier()
            volume = VolumeController()
            actions = ActionManager()
            ui = UI()
            fps_counter = FPSCounter()
            
            
            app_logger.info("Camera tracking loop activated.")
            self.status = "Running"
            
            while self.active:
                success, frame = camera.read()
                if not success:
                    self.status = "Camera read failed"
                    time.sleep(0.1)
                    continue
                    
                self.fps = fps_counter.update()
                
                # Detect hands
                hands = tracker.detect(frame, draw=False)
                current_time = time.time()
                
                if hands:
                    hand = hands[0]
                    self.hand_label = hand.label
                    self.gesture = classifier(hand)
                    app_logger.gesture(self.gesture)
                    
                    thumb = hand[4]
                    index = hand[8]
                    cx = (thumb.x + index.x) // 2
                    cy = (thumb.y + index.y) // 2
                    distance = hand.distance(4, 8)
                    
                    # Draw custom pinch connection lines with HUD colors
                    cv2.circle(frame, (thumb.x, thumb.y), 8, (180, 0, 255), cv2.FILLED, cv2.LINE_AA)
                    cv2.circle(frame, (index.x, index.y), 8, (180, 0, 255), cv2.FILLED, cv2.LINE_AA)
                    cv2.line(frame, (thumb.x, thumb.y), (index.x, index.y), (255, 240, 0), 2, cv2.LINE_AA)
                    cv2.circle(frame, (cx, cy), 6, (0, 255, 100), cv2.FILLED, cv2.LINE_AA)
                    
                    # Volume control distance mapping
                    distance = max(
                        config.PINCH_MIN_DISTANCE,
                        min(
                            config.PINCH_MAX_DISTANCE,
                            distance
                        )
                    )
                    
                    volume.set_by_distance(distance)
                    self.status = f"Volume: {volume.get_percentage()}%"
                    
                    # Cooldown checks for web browser commands and screenshots
                    if current_time - actions.last_action > config.ACTION_COOLDOWN:
                        if self.gesture == config.THUMB_UP:
                            actions._update()
                            self.action = "Opening ChatGPT..."
                            self.status = self.action
                            app_logger.action(self.action)
                            _action_queue.put_nowait(("open_chatgpt", lambda: _open_url(config.CHATGPT_URL)))
                        elif self.gesture == config.PEACE:
                            actions._update()
                            self.action = "Taking Screenshot..."
                            self.status = self.action
                            app_logger.action(self.action)
                            def _do_screenshot(a=actions):
                                import pyautogui
                                from datetime import datetime
                                filename = datetime.now().strftime("Screenshot_%Y%m%d_%H%M%S.png")
                                filepath = config.SCREENSHOT_DIR / filename
                                pyautogui.screenshot().save(filepath)
                                a_logger = logging.getLogger("GestureControls")
                                a_logger.info(f"Screenshot saved: {filename}")
                            _action_queue.put_nowait(("screenshot", _do_screenshot))
                        elif self.gesture == config.ROCK:
                            actions._update()
                            self.action = "Opening YouTube..."
                            self.status = self.action
                            app_logger.action(self.action)
                            _action_queue.put_nowait(("open_youtube", lambda: _open_url(config.YOUTUBE_URL)))
                        else:
                            self.action = "Volume Control"
                else:
                    self.gesture = config.UNKNOWN
                    self.action = "Waiting..."
                    self.hand_label = "None"
                    self.status = "Show Hand"
                    
                self.volume_percentage = volume.get_percentage()
                
                # Overlay dynamic cyberpunk HUD
                frame = ui.update(
                    frame=frame,
                    fps=self.fps,
                    gesture=self.gesture,
                    action=self.action,
                    hand_obj=hands[0] if hands else None,
                    volume=self.volume_percentage,
                    status=self.status
                )
                
                # Convert processed OpenCV matrix to JPEG bytes for MJPEG streamer
                success_encode, jpeg_buffer = cv2.imencode('.jpg', frame)
                if success_encode:
                    self.latest_jpeg = jpeg_buffer.tobytes()
                    
                
        except Exception as e:
            app_logger.error(f"Engine exception: {e}")
            self.status = f"Fatal Error: {e}"
        finally:
            app_logger.info("Tearing down camera engine modules...")
            app_logger.shutdown()
            
            if tracker:
                try: tracker.close()
                except Exception: pass
            if camera:
                try: camera.release()
                except Exception: pass
                
            # cv2.destroyAllWindows()  # Not needed — no GUI window in web mode
            
            self.active = False
            self.latest_jpeg = None
            self.fps = 0.0
            self.hand_label = "None"
            self.gesture = "UNKNOWN"
            self.action = "None"
            self.status = "Stopped"

# Instantiate Singleton engine
engine = GestureEngine()


# ==========================================================
# CONFIGURATION AND INPUT MODELS
# ==========================================================

class ConfigModel(BaseModel):
    camera_index: int
    detection_confidence: float
    cooldown: float
    chatgpt_url: str
    youtube_url: str

class VolumeModel(BaseModel):
    value: int


# ==========================================================
# REST API ENDPOINTS
# ==========================================================

@app.get("/api/config")
def get_config():
    return {
        "camera_index": config.CAMERA_INDEX,
        "detection_confidence": config.DETECTION_CONFIDENCE,
        "cooldown": config.ACTION_COOLDOWN,
        "chatgpt_url": config.CHATGPT_URL,
        "youtube_url": config.YOUTUBE_URL
    }

@app.post("/api/config")
def set_config(data: ConfigModel):
    config.CAMERA_INDEX = data.camera_index
    config.DETECTION_CONFIDENCE = data.detection_confidence
    config.ACTION_COOLDOWN = data.cooldown
    config.CHATGPT_URL = data.chatgpt_url
    config.YOUTUBE_URL = data.youtube_url
    
    logger.info("Configuration parameters updated by Web client.")
    
    # If engine is already running, restarting it is recommended to apply camera index or detector confidence.
    if engine.active:
        logger.info("Active camera engine detected. Re-running engine to apply configuration changes...")
        engine.stop()
        # Wait a moment for teardown
        time.sleep(1.0)
        engine.start()
        
    return {"status": "success"}

@app.post("/api/toggle")
def toggle_engine():
    if engine.active:
        engine.stop()
        logger.info("Camera runner engine stopped via Dashboard request.")
    else:
        engine.start()
        logger.info("Camera runner engine started via Dashboard request.")
    
    # Wait briefly for state transition
    time.sleep(0.5)
    return {"engine_active": engine.active}

@app.get("/api/test_action/{name}")
def test_action(name: str):
    """Manually trigger an action for testing purposes."""
    if name == "chatgpt":
        _action_queue.put_nowait(("open_chatgpt", lambda: _open_url(config.CHATGPT_URL)))
        return {"status": "queued", "action": "open_chatgpt"}
    elif name == "youtube":
        _action_queue.put_nowait(("open_youtube", lambda: _open_url(config.YOUTUBE_URL)))
        return {"status": "queued", "action": "open_youtube"}
    else:
        return {"status": "unknown action"}

@app.post("/api/volume")
def set_volume(volume_data: VolumeModel):
    # Set OS volume level manually via slider request
    try:
        vc = VolumeController()
        vc.set_percentage(volume_data.value)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screenshots")
def get_screenshots():
    # Fetch list of saved screenshot file names
    try:
        files = sorted(
            config.SCREENSHOT_DIR.glob("*.png"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        return [f.name for f in files]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/screenshots/{name}")
def delete_screenshot(name: str):
    # Securely delete a screenshot to avoid directory traversal
    try:
        safe_path = (config.SCREENSHOT_DIR / name).resolve()
        if safe_path.parent == config.SCREENSHOT_DIR.resolve() and safe_path.exists():
            safe_path.unlink()
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# LIVE MJPEG VIDEO STREAM YIELD
# ==========================================================

async def frame_generator() -> Generator[bytes, None, None]:
    """Generates JPEG boundaries for MJPEG streaming in HTML img tag."""
    while True:
        if engine.active and engine.latest_jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + engine.latest_jpeg + b'\r\n')
        else:
            # Yield transparent tiny 1x1 jpeg to avoid broken image symbol in browser
            tiny_gif = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
            yield (b'--frame\r\n'
                   b'Content-Type: image/gif\r\n\r\n' + tiny_gif + b'\r\n')
        # Stream around 25 FPS
        await asyncio.sleep(0.04)

@app.get("/api/video_feed")
def video_feed():
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")


# ==========================================================
# SERVER EVENT STREAM (SSE) FOR TELEMETRY & EVENT LOGS
# ==========================================================

@app.get("/api/events")
def event_stream(request: Request):
    async def sse_event_generator():
        while True:
            # Check connection disconnect
            if await request.is_disconnected():
                break
                
            # Telemetry Payload
            telemetry = {
                "type": "telemetry",
                "fps": float(engine.fps),
                "hand": str(engine.hand_label),
                "gesture": str(engine.gesture),
                "action": str(engine.action),
                "volume": int(engine.volume_percentage),
                "status": str(engine.status),
                "engine_active": bool(engine.active)
            }
            yield f"data: {json.dumps(telemetry)}\n\n"
            
            # Fetch log queues and stream lines
            while not log_queue.empty():
                try:
                    log_line = log_queue.get_nowait()
                    log_payload = {
                        "type": "log",
                        "message": log_line
                    }
                    yield f"data: {json.dumps(log_payload)}\n\n"
                except Exception:
                    break
                    
            await asyncio.sleep(0.1)  # 10Hz updates

    return StreamingResponse(sse_event_generator(), media_type="text/event-stream")


# ==========================================================
# STATIC FILES SERVING
# ==========================================================

# Map screenshots directory to serve saved images to client gallery
app.mount("/screenshots", StaticFiles(directory=str(config.SCREENSHOT_DIR)), name="screenshots")

# Serve UI HTML, JS, CSS dashboard files (HTML main is set as index)
app.mount("/", StaticFiles(directory="web", html=True), name="web")


# ==========================================================
# RUN SERVER PROGRAMMATICALLY
# ==========================================================

if __name__ == "__main__":
    import uvicorn
    
    # Auto-activate engine on startup
    engine.start()
    
    print("\n" + "="*60)
    print(" GESTURE CONTROLS DASHBOARD WEB SERVER IS LAUNCHING")
    print("="*60)
    print(" Access Web Panel: http://localhost:8000")
    print(" Quit Server: CTRL+C inside the terminal")
    print("="*60 + "\n")
    
    try:
        uvicorn.run("web_app:app", host="127.0.0.1", port=8000, log_level="warning")
    finally:
        engine.stop()
        print("\nGesture controls dashboard server shutdown completed.")
