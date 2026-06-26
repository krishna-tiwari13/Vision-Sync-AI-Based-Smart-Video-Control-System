#  VisionSync: AI-Based Smart Video Control System

An AI-powered smart video control system that enables hands-free media interaction using **computer vision**, **hand gesture recognition**, **face detection**, and **voice commands**.

---

##  Overview

VisionSync allows users to control video playback without using a keyboard or mouse. It automatically pauses the video when the user is not looking at the screen, supports gesture and voice-based controls, and reminds users to take breaks for healthier screen usage.

---

##  Features

-  Face Detection
  - Automatically pauses the video when the user leaves.
  - Resumes playback when the user returns.

-  Hand Gesture Control
  - Increase volume
  - Decrease volume
  - Next video
  - Previous video
  - Snap gesture to close the video

-  Voice Commands
  - Play
  - Pause
  - Next
  - Previous

-  Screen Time Monitoring
  - Custom watch timer
  - Break reminder to reduce eye strain

- Real-time Computer Vision
  - Live webcam processing
  - AI-based hand landmark detection using MediaPipe

---

##  Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- SpeechRecognition
- Keyboard
- Threading

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/krishna-tiwari13/Vision-Sync-AI-Based-Smart-Video-Control-System.git
```

### 2. Open the project

```bash
cd Vision-Sync-AI-Based-Smart-Video-Control-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the project

```bash
python main.py
```

---

## 🎮 Controls

| Action | Control |
|---------|---------|
| Play / Pause | Voice Command or Face Detection |
| Volume Up | Increase thumb-index distance |
| Volume Down | Decrease thumb-index distance |
| Next Video | Two fingers up |
| Previous Video | Three fingers up |
| Close Video | Snap gesture |

---

## Workflow

1. Capture live webcam video.
2. Detect the user's face.
3. Pause or resume the video based on attention.
4. Detect hand gestures using MediaPipe.
5. Execute media controls using PyAutoGUI.
6. Listen for voice commands in a background thread.
7. Monitor screen time and display a break reminder.

##  Developer

**Krishna Tiwari**


GitHub: https://github.com/krishna-tiwari13

---

## ⭐ If you found this project useful, consider giving it a Star!