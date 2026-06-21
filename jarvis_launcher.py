#!/usr/bin/env python3
"""
JARVIS Clap Launcher
====================
Run this script in the background. When it detects a double-clap,
it opens your JARVIS assistant in the browser.

Requirements:
  pip install pyaudio numpy

On Windows: pip install pyaudio
On Mac:     brew install portaudio && pip install pyaudio
On Linux:   sudo apt install python3-pyaudio portaudio19-dev

Usage:
  python jarvis_launcher.py
  
To run on startup (Windows):
  - Press Win+R, type: shell:startup
  - Create a shortcut to: pythonw jarvis_launcher.py
  - Set "Start in" to the folder where this file is

To run on startup (Mac):
  - Add to Login Items in System Settings
"""

import pyaudio
import numpy as np
import webbrowser
import time
import os
import sys
import subprocess

# ─── CONFIG ───────────────────────────────────────────────────────────────────
JARVIS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.html")
CLAP_THRESHOLD = 3000       # Volume threshold for a clap (raise if too sensitive)
DOUBLE_CLAP_GAP = 0.6       # Max seconds between two claps to count as double
MIN_CLAP_GAP = 0.08         # Min seconds between claps (avoid single clap echo)
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
COOLDOWN = 3.0              # Seconds to wait after opening before listening again

# ─── AUDIO DETECTION ──────────────────────────────────────────────────────────
def is_clap(audio_chunk, threshold=CLAP_THRESHOLD):
    """Check if an audio chunk contains a clap (loud, sharp sound)."""
    samples = np.frombuffer(audio_chunk, dtype=np.int16)
    return np.max(np.abs(samples)) > threshold

def open_jarvis():
    """Open the JARVIS HTML file in the default browser."""
    file_url = f"file:///{JARVIS_FILE.replace(os.sep, '/')}"
    print(f"[JARVIS] Opening: {file_url}")
    webbrowser.open(file_url)

def listen_for_claps():
    """Main loop: listen for double-clap."""
    p = pyaudio.PyAudio()
    
    # Find input device
    device_index = None
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            device_index = i
            break
    
    if device_index is None:
        print("[JARVIS] No microphone found!")
        return
    
    print("[JARVIS] ✅ Clap detector running...")
    print(f"[JARVIS] 👏 Double-clap to open JARVIS (threshold: {CLAP_THRESHOLD})")
    print("[JARVIS] Press Ctrl+C to stop\n")
    
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
        input_device_index=device_index
    )
    
    last_clap_time = 0
    clap_count = 0
    last_open_time = 0
    
    try:
        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            now = time.time()
            
            if is_clap(data):
                gap = now - last_clap_time
                
                if gap > MIN_CLAP_GAP:
                    if gap <= DOUBLE_CLAP_GAP and clap_count >= 1:
                        # Double clap detected!
                        clap_count = 0
                        if now - last_open_time > COOLDOWN:
                            print("[JARVIS] 👏👏 Double clap detected! Opening JARVIS...")
                            open_jarvis()
                            last_open_time = now
                    else:
                        clap_count = 1
                        print("[JARVIS] 👏 First clap... waiting for second...")
                    
                    last_clap_time = now
            
            # Reset if too long since first clap
            if clap_count > 0 and (now - last_clap_time) > DOUBLE_CLAP_GAP:
                clap_count = 0
    
    except KeyboardInterrupt:
        print("\n[JARVIS] Stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# ─── SENSITIVITY TESTER ───────────────────────────────────────────────────────
def test_sensitivity():
    """Run this to find the right CLAP_THRESHOLD for your mic."""
    print("Testing microphone sensitivity...")
    print("Clap near your mic and watch the values.\n")
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    
    try:
        for _ in range(200):
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)
            vol = np.max(np.abs(samples))
            bar = '█' * int(vol / 500)
            print(f"\rVolume: {vol:5d} {bar:<30}", end='')
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
    print("\n\nSet CLAP_THRESHOLD between your background noise level and clap level.")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_sensitivity()
    else:
        # Check if JARVIS file exists
        if not os.path.exists(JARVIS_FILE):
            print(f"[JARVIS] ⚠️  jarvis.html not found at: {JARVIS_FILE}")
            print("[JARVIS] Make sure jarvis.html is in the same folder as this script!")
            input("Press Enter to exit...")
            sys.exit(1)
        
        listen_for_claps()
