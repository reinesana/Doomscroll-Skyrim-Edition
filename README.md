# Doomscroll Skyrim Edition

**A CV productivity tool that plays Skyrim Skeleton mode whenever you doomscroll or lose focus.**

![Skyrim Skeleton](https://github.com/user-attachments/assets/d06ccf2f-0b9d-4fdf-8a95-6117c0d77c15)

---

## Introduction

**Doomscrolling: Skyrim Edition** is a CV productivity tool inspired by the **Skeleton** trend on **TikTok** and my previous doomscrolling tool: **Charlie Kirkification**. Designed for laptop-based work only. Using your webcam, the program tracks your eye gaze in real time to detect when you're looking down at your phone (aka doomscrolling).

**Note**: this tool does not work for activities like writing, reading books, or other offline tasks since it uses gaze detection to detect doomscrolling

---

## How it works

1. Your webcam feed is processed in real time using MediaPipe's face landmarker
2. The program uses eye gaze blendshapes to detect when you're looking down
3. If you doomscroll for longer than a set threshold:
   - The Skyrim Skeleton interferes with your doomscrolling

---

## System Requirements
- Operating System: macOS using `osascript`, `QuickTime Player`
- Python: 3.9+
- Permissions: Camera access must be enabled for the terminal running the script.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/reinesana/Doomscroll-Skyrim-Edition.git
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the face landmarker model
```bash
curl -o assets/face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

### 5. Run the program
```bash
python main.py
```

---

## Configuration

You can customize how the system behaves by editing the configuration values in `main.py`.

### `timer`
The minimum amount of time the user must be “looking down” before triggering the program. This acts as a grace period.
- Lower values → triggers faster
- Higher values → longer grace period before triggering
  
```python
timer = 2.0  
```

### `start_threshold`
The gaze score required to start the video.
- Higher value → more strict, requires stronger downward gaze to trigger

```python
start_threshold = 0.4
```

### `maintain_threshold`
The threshold used while the video is playing. Lower than `start_threshold` so the video keeps playing unless you clearly look up.

```python
maintain_threshold = 0.3
```

---

License @ MIT  
