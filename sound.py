# This file plays the game's sound effects
import os
import subprocess
import sys

SOUND_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "sounds"
)

try:
    import winsound  # Built into Python on Windows
except ImportError:
    winsound = None


# Play sounds/<name>.wav without freezing the game
def play(name, window=None):
    path = os.path.join(SOUND_FOLDER, name + ".wav")

    if not os.path.exists(path):
        return

    try:
        if winsound is not None:
            winsound.PlaySound(
                path,
                winsound.SND_FILENAME
                | winsound.SND_ASYNC
                | winsound.SND_NODEFAULT
            )

        elif sys.platform == "darwin":
            subprocess.Popen(["afplay", path])

        else:
            subprocess.Popen(
                ["aplay", "-q", path],
                stderr=subprocess.DEVNULL
            )

    except (OSError, RuntimeError):
        # No audio player available, fall back to the system beep
        if window is not None:
            window.bell()
