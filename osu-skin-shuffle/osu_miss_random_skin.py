"""
osu!lazer: random skin change on Miss
------------------------------------------
On every Miss (100 and 50 do NOT count) the key combo
Ctrl+Shift+R is sent (osu!'s hotkey for "random skin").

REQUIREMENTS:
1. Install and run tosu (https://tosu.app) — it reads the game
   data from memory and exposes it over WebSocket. Works with
   osu!lazer and stable. Just launch tosu.exe, it will find the
   running osu! automatically and open a server on 127.0.0.1:24050.
2. Launch osu!lazer.
3. Run this script (python osu_miss_random_skin.py).
4. The websockets and keyboard libraries will be installed
   automatically on first run.

IMPORTANT:
- If osu!lazer is running as administrator, this script must
  also be run as administrator — otherwise Windows won't allow
  sending keystrokes to a privileged window.
- The JSON structure returned by tosu may differ slightly
  between versions. If the script doesn't react to misses, open
  http://127.0.0.1:24050/json in a browser while playing and
  check the path to the miss counter matches what's used below.
"""

import asyncio
import json
import subprocess
import sys


def ensure_installed(module_name, pip_name=None):
    try:
        __import__(module_name)
    except ImportError:
        pip_name = pip_name or module_name
        print(f"Installing {pip_name}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pip_name, "--break-system-packages"]
        )


ensure_installed("websockets")
ensure_installed("keyboard")

import websockets  # noqa: E402
import keyboard  # noqa: E402

TOSU_WS_URL = "ws://127.0.0.1:24050/websocket/v2"
HOTKEY = "ctrl+shift+r"


def get_miss_count(data: dict):
    """Extracts the miss count from tosu's JSON. Returns None if not found."""
    try:
        return data["play"]["hits"]["0"]
    except (KeyError, TypeError):
        return None


def get_state_name(data: dict):
    try:
        return data["state"]["name"]
    except (KeyError, TypeError):
        return None


async def listen():
    print("Connecting to tosu...")
    async with websockets.connect(TOSU_WS_URL) as ws:
        print("Connected! Waiting for gameplay to start (launch a map in osu!lazer)...")
        last_miss_count = None

        async for message in ws:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                continue

            state_name = get_state_name(data)

            # Not in gameplay (menu, results screen, etc.) — reset the
            # counter so the start of a new map isn't counted as a "miss".
            if state_name != "play":
                last_miss_count = None
                continue

            miss_count = get_miss_count(data)
            if miss_count is None:
                continue

            if last_miss_count is None:
                last_miss_count = miss_count
                continue

            if miss_count > last_miss_count:
                print(f"Miss! ({last_miss_count} -> {miss_count}) -> {HOTKEY}")
                keyboard.send(HOTKEY)

            last_miss_count = miss_count


async def main():
    while True:
        try:
            await listen()
        except (ConnectionRefusedError, OSError) as e:
            print(f"tosu is not responding ({e}). Make sure tosu is running. Retrying in 3s...")
            await asyncio.sleep(3)
        except websockets.exceptions.ConnectionClosed:
            print("Connection to tosu lost. Reconnecting in 3s...")
            await asyncio.sleep(3)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
