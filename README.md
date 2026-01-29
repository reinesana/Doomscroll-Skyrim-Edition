# Doomscroll Skyrim Edition

**A CV productivity tool that plays Skyrim Skeleton mode whenever you doomscroll or lose focus.**

![Skyrim Skeleton](https://github.com/user-attachments/assets/d06ccf2f-0b9d-4fdf-8a95-6117c0d77c15)

---

## Introduction

**Doomscrolling: Skyrim Edition** is a CV productivity tool inspired by the **Skeleton** trend on **TikTok** and my previous doomscrolling tool: **Charlie Kirkification**. Designed for laptop-based work only. Using your webcam, the program tracks your eye and iris movement in real time to detect when you’re looking down at your phone (aka doomscrolling).

**Note**: this tool does not work for activities like writing, reading books, or other offline tasks since it uses iris movement to detect doomscrolling

---

## How it works

1. Your webcam feed is processed in real time using face mesh + iris tracking  
2. The program checks whether your iris movement suggests you’re looking at your phone
3. If you doomscroll for longer than a set threshold:
   -  The Skyrim Skeleton interferes with your doomscrolling

---

## Sytem Requirements
- Operating System: macOS using `osascript`,  `QuickTime Player`
- Python: 3.9 - 3.12. Not compatible with Python 3.13
- Permissions: Camera access must be enabled for the terminal running the script.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/reinesana/Doomscroll-Skyrim-Edition.git
```

### 2. Install dependencies
Make sure you are using **Python 3.9-3.12+** on your system. Not compatible with Python 3.13.

```bash
pip install -r requirements.txt
```

### 3. Run the program
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

### `looking_down_threshold`
The minimum iris position required to consider the user as looking down.
Lower value → more strict and requires stronger downward gaze
Higher value → more sensitive 
  
Adjust `looking_down_threshold` to control the sensitivity of iris detection.
```python
looking_down_threshold = 0.25

```

### `debounce_threshold`
The minimum threshold required for the system to exit the “looking down” state before the program resets.
- Lower value → video stops more easily (more strict while playing)
- Higher value → video stays on longer (more forgiving while playing)

Adjust `debounce_threshold` to control how much upward eye movement is required before the program resets.
```python
debounce_threshold = 0.45
```

---

License @ MIT  
