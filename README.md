# FingerCommander

A Linux utility that uses your webcam to recognize hand gestures and run system commands like opening VS Code, locking the screen, or shutting down — all controlled by your fingers.

Powered by **OpenCV** + **MediaPipe**


## 📽️ How It Works

This app captures live webcam footage, detects your hand using MediaPipe, and matches the finger positions to predefined gestures. If a gesture matches, a mapped system command is executed (with a cooldown to avoid rapid repeats).

##  Setup Instructions

Make sure Python 3 is installed (optionally create a venv), then run:

```bash
pip install opencv-python mediapipe
```


### 2. Project Structure

```
FingerCommander/
│
├── gestures.py              # Contains gesture-command mappings
├── gesture_control.py       # Main script 
├── venv/                    # (optional) your virtual environment
└── README.md
```

### Define Your Gestures

Edit the `gestures.py` file like so:

```python
GESTURE_COMMANDS = {
    "peace": ("code", [0, 1, 1, 0, 0]),  # VS Code
    "middle": ("shutdown now", [0, 0, 1, 0, 0]),  # Shutdown
    "pinky": ("gnome-screensaver-command -l", [0, 0, 0, 0, 1])  # Lock screen
}
```

Each entry is a tuple of:

* Shell command to execute
* Finger pattern list: `[thumb, index, middle, ring, pinky]`
  (`1` for raised, `0` for folded)

###  Run the App

If you’re using a virtual environment:

```bash
source venv/bin/activate
python gesture_control.py
```

Quit the app by pressing `q`.


## Optional Custom Command Alias

Create a quick command (`camsequence`) to launch it:

```bash
alias camsequence='cd <project-dir> && source venv/bin/activate && python gesture_control.py'
```

Then just type `camsequence` in your terminal.



## 👨‍💻 Author

Developed by [epicboi-deepubhai](https://github.com/epicboi-deepubhai)
