#!/usr/bin/env python3
"""
JARVIS Voice Launcher — "Hello Piko" wake word + voice commands
==================================================================
Run this script in the background. Say "Hello Piko" followed by what
you want (e.g. "Hello Piko, remind me to submit the lab report") and
it opens JARVIS with that command already typed in and sent.

You can also just say "Hello Piko" alone to simply open JARVIS.

Requirements:
  pip install SpeechRecognition pyaudio

On Windows: pip install pyaudio (use Python 3.11 if 3.13/3.14 fails to build)
On Mac:     brew install portaudio && pip install pyaudio
On Linux:   sudo apt install python3-pyaudio portaudio19-dev

Usage:
  python jarvis_voice.py

To run on startup (Windows):
  - Press Win+R, type: shell:startup
  - Create a shortcut to: pythonw jarvis_voice.py
  - Set "Start in" to the folder where this file is

To run on startup (Mac):
  - Add to Login Items in System Settings
"""

import speech_recognition as sr
import webbrowser
import time
import os
import sys
import re
from urllib.parse import quote

# ─── CONFIG ───────────────────────────────────────────────────────────────────
JARVIS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.html")
WAKE_WORDS = ["hello piko", "hey piko", "piko"]   # any of these will trigger it
COOLDOWN = 3.0                                     # seconds to wait after opening before listening again
LISTEN_TIMEOUT = 5                                 # max seconds to wait for a phrase to start
PHRASE_TIME_LIMIT = 4                              # max seconds for the wake-word phrase
COMMAND_TIME_LIMIT = 8                             # max seconds to capture the follow-up command

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def open_jarvis(command=None):
    """Open the JARVIS HTML file in the default browser, optionally with a voice command."""
    file_url = f"file:///{JARVIS_FILE.replace(os.sep, '/')}"
    if command:
        file_url += f"?say={quote(command)}"
        print(f"[JARVIS] Opening with command: \"{command}\"")
    else:
        print(f"[JARVIS] Opening: {file_url}")
    webbrowser.open(file_url)

def extract_command(text):
    """Strip the wake word out of a heard phrase, return whatever command remains."""
    low = text.lower()
    for w in sorted(WAKE_WORDS, key=len, reverse=True):
        idx = low.find(w)
        if idx != -1:
            remainder = text[idx+len(w):].strip()
            # remove leading punctuation/filler like ", " or "comma"
            remainder = re.sub(r'^[\s,،.!:-]+', '', remainder)
            return remainder
    return ""

def heard_wake_word(text):
    """Check if the recognized text contains a wake word."""
    text_low = text.lower().strip()
    return any(w in text_low for w in WAKE_WORDS)

# ─── MAIN LISTEN LOOP ─────────────────────────────────────────────────────────
def listen_for_wake_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("[JARVIS] Calibrating for background noise... stay quiet for a moment.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.5)

    print("[JARVIS] ✅ Voice listener running...")
    print(f"[JARVIS] 🎙️  Say 'Hello Piko' to open JARVIS")
    print(f"[JARVIS] 🎙️  Or say 'Hello Piko, remind me to study' to open AND send a command")
    print("[JARVIS] Press Ctrl+C to stop\n")

    last_open_time = 0

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)

            try:
                text = recognizer.recognize_google(audio)
                print(f"[JARVIS] Heard: \"{text}\"")

                if heard_wake_word(text):
                    now = time.time()
                    if now - last_open_time <= COOLDOWN:
                        print("[JARVIS] (cooldown active, ignoring)")
                        continue

                    # Check if a command was already included in the same phrase
                    command = extract_command(text)

                    # If nothing came after the wake word, listen again briefly for the command
                    if not command:
                        print("[JARVIS] 🎯 Wake word detected! Listening for your command...")
                        try:
                            with mic as source:
                                cmd_audio = recognizer.listen(source, timeout=3, phrase_time_limit=COMMAND_TIME_LIMIT)
                            command = recognizer.recognize_google(cmd_audio)
                            print(f"[JARVIS] Command heard: \"{command}\"")
                        except sr.WaitTimeoutError:
                            print("[JARVIS] No command heard — just opening JARVIS.")
                            command = None
                        except sr.UnknownValueError:
                            print("[JARVIS] Couldn't understand the command — just opening JARVIS.")
                            command = None

                    open_jarvis(command if command else None)
                    last_open_time = time.time()

            except sr.UnknownValueError:
                # Speech was unintelligible — totally normal, just ignore
                pass
            except sr.RequestError as e:
                print(f"[JARVIS] ⚠️ Speech service error: {e}")
                print("[JARVIS] Check your internet connection. Retrying in 3s...")
                time.sleep(3)

        except sr.WaitTimeoutError:
            # No speech detected in the timeout window — keep listening
            pass
        except KeyboardInterrupt:
            print("\n[JARVIS] Stopped.")
            break
        except Exception as e:
            print(f"[JARVIS] Error: {e}")
            time.sleep(1)

# ─── MIC TESTER ───────────────────────────────────────────────────────────────
def test_microphone():
    """List available microphones and do a quick recognition test."""
    print("Available microphones:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{i}] {name}")
    print()

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Testing... say something in the next 5 seconds:")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            text = recognizer.recognize_google(audio)
            print(f"\n✅ Heard you say: \"{text}\"")
            print("Microphone is working correctly!")
        except sr.WaitTimeoutError:
            print("\n⚠️ No speech detected. Check your microphone is connected and not muted.")
        except sr.UnknownValueError:
            print("\n⚠️ Heard audio but couldn't understand it. Try speaking more clearly.")
        except sr.RequestError as e:
            print(f"\n⚠️ Could not reach speech service: {e}")
            print("Check your internet connection (this feature needs internet).")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_microphone()
    else:
        if not os.path.exists(JARVIS_FILE):
            print(f"[JARVIS] ⚠️  jarvis.html not found at: {JARVIS_FILE}")
            print("[JARVIS] Make sure jarvis.html is in the same folder as this script!")
            input("Press Enter to exit...")
            sys.exit(1)

        listen_for_wake_word()
