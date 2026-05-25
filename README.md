# HandFlow - Gesture Controlled Mouse

HandFlow is a Python-based virtual mouse controller that uses your webcam and hand gestures to control your computer mouse in real time.

It uses:
- OpenCV for webcam capture and rendering
- MediaPipe for hand tracking
- Mouse library for controlling the cursor

## Features

- Real-time hand tracking
- Smooth mouse movement
- Left click gesture
- Right click gesture
- Adjustable sensitivity and smoothing
- Deadzone filtering for stability

---

## How It Works

### Mouse Movement
- The wrist/base landmark (`landmark[0]`) controls the mouse movement.
- Cursor movement is smoothed using linear interpolation (`lerp`).

### Left Click
- Touching the thumb and index finger triggers a left click.

### Right Click
- Touching the thumb and middle finger triggers a right click.

---

## Controls

| Gesture | Action |
|---|---|
| Thumb + Index Finger | Left Click |
| Thumb + Middle Finger | Right Click |
| Move Hand | Move Cursor |
| Press `Q` | Quit Application |

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Nullit13/handflow.git
cd handflow
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

---

## Configuration

You can modify these values in the script:

```python
sensitivity = 3
smoothTime = 0.25
deadzone = 1
```

### Description
- `sensitivity` → Cursor movement speed
- `smoothTime` → Cursor smoothing amount
- `deadzone` → Minimum movement before cursor moves

---

## Notes

- Ensure your webcam is connected and accessible.
- Good lighting improves hand detection accuracy.
- Screen resolution is currently set manually:

```python
screen_w, screen_h = 1920, 1080
```

Adjust this to match your monitor resolution.

---

## Future Improvements

- Multi-hand support
- Gesture customization
- Drag-and-drop gestures
- Scroll gesture support
- Automatic screen resolution detection

---

## License

This project is open-source and free to use.