import cv2
import time
import pyautogui
import keyboard
import mediapipe as mp
import numpy as np
import math
import threading
import speech_recognition as sr

# -------- VOICE CONTROL THREAD --------
def listen_for_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Voice control active...")
        while True:
            try:
                audio = r.listen(source, phrase_time_limit=2)
                command = r.recognize_google(audio).lower()
                print(f"Voice Command: {command}")
                if "next" in command:
                    pyautogui.hotkey('shift', 'n')
                elif "previous" in command or "back" in command:
                    pyautogui.hotkey('shift', 'p')
                elif "play" in command or "pause" in command:
                    pyautogui.press('space')
            except:
                pass

# -------- FACE SETUP --------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    try:
        user_minutes = int(input("Enter watch time (in minutes): "))
        if user_minutes > 0: break
        else: print("Enter positive number!")
    except: print("Invalid input!")

watch_limit = user_minutes * 60

# -------- HAND SETUP --------
mp_hands = mp.solutions.hands   
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

start_time = time.time()
alert_shown = False
prev_distance = 1000
snap_cooldown = 0
not_looking_start = None
paused = False
last_action_time = 0
gesture_time = 0

print("Open your video (YouTube/VLC). Press ENTER here to start...")
keyboard.wait("enter")

# START VOICE THREAD
threading.Thread(target=listen_for_voice, daemon=True).start()

print("System Started!")

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    current_time = time.time()
    h, w, c = frame.shape

    # -------- FACE DETECTION (Auto-Pause) --------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        if paused and current_time - last_action_time > 2:
            pyautogui.press("space")
            paused = False
            last_action_time = current_time
        not_looking_start = None
        status = "Watching "
    else:
        if not_looking_start is None: not_looking_start = current_time
        elapsed = current_time - not_looking_start
        if elapsed > 0.5 and not paused and current_time - last_action_time > 2:
            pyautogui.press("space")
            paused = True
            last_action_time = current_time
            status = "PAUSED ⏸"
        else:
            status = "Not Watching..."

    # -------- WATCH TIME ALERT --------
    if current_time - start_time > watch_limit and not alert_shown:
        pyautogui.alert("⚠️ ALERT! Take a break. Protect your eyes!")
        alert_shown = True

    # -------- HAND GESTURE DETECTION --------
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB) #This runs the pre-trained neural network on your frame

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: #MediaPipe provides landmarks in normalized coordinates (0.0 to 1.0)
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            if lmList:
                # 1. VOLUME CONTROL
                x1, y1 = lmList[4][1], lmList[4][2]   # Thumb
                x2, y2 = lmList[8][1], lmList[8][2]   # Index
                vol_len = np.hypot(x2 - x1, y2 - y1) #This is a mathematical function that calculates the Euclidean distance between the two points

                if current_time - gesture_time > 0.3: #Without it, the code would trigger a volumeup command 30 times per second
                    if vol_len > 120:
                        pyautogui.press("volumeup")
                        gesture_time = current_time
                    elif vol_len < 40:
                        pyautogui.press("volumedown")
                        gesture_time = current_time

                # 2. VIDEO CONTROL (NEXT / PREVIOUS)
                index_up = lmList[8][2] < lmList[6][2]
                middle_up = lmList[12][2] < lmList[10][2]
                ring_up = lmList[16][2] < lmList[14][2]

                if current_time - gesture_time > 1.5:
                    #  Two Fingers Up = Next
                    if index_up and middle_up and not ring_up:
                        pyautogui.hotkey('shift', 'n')
                        print("Gesture: Next Video")
                        gesture_time = current_time
                    #  Three Fingers Up = Previous
                    elif index_up and middle_up and ring_up:
                        pyautogui.hotkey('shift', 'p')
                        print("Gesture: Previous Video")
                        gesture_time = current_time

                # 3. SNAP DETECTION (ALT+F4)
                snap_dist = math.hypot(lmList[12][1] - lmList[4][1], lmList[12][2] - lmList[4][2])
                if snap_dist < 30 and prev_distance > 80:
                    if current_time - snap_cooldown > 0.5:
                        print(" SNAP! Closing Video")
                        pyautogui.hotkey('alt', 'f4')
                        snap_cooldown = current_time
                prev_distance = snap_dist

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS) #maps the wireframe skeleton onto your hand for tracking your fingers accurately

    # -------- UI --------
    color = (0, 255, 0) if not paused else (0, 0, 255)
    cv2.putText(frame, status, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("AI Control System", frame)

    if cv2.waitKey(1) & 0xFF == 27: # ESC to quit, It waits 1 millisecond for a keyboard input.
        break

cap.release() #This is crucial. It tells the operating system to stop hogging the webcam hardware
cv2.destroyAllWindows()#Closes any GUI windows created by OpenCV, preventing "ghost" windows from remaining open in the background.