# osu-miss-random-skin

Automatically triggers osu!'s **random skin** hotkey (`Ctrl+Shift+R`) every time you get a **Miss** while playing **osu!lazer** (or stable). 100s and 50s do not trigger it — only actual misses.

It works by reading live gameplay data from [tosu](https://tosu.app), a memory-reading tool for osu!, over its WebSocket API, and sending the hotkey via the [`keyboard`](https://pypi.org/project/keyboard/) library.

## How it works

1. [tosu](https://tosu.app) reads osu!'s game memory and exposes real-time gameplay state (combo, hit counts, etc.) over a local WebSocket server (`ws://127.0.0.1:24050/websocket/v2`).
2. This script connects to that WebSocket and watches the miss counter (`play.hits\\\\\\\["0"]`).
3. Whenever the miss counter increases during active gameplay, it sends `Ctrl+Shift+R`.
4. The counter resets whenever you leave gameplay (menu, results screen, retry), so starting a new map is never mistaken for a miss.

## Requirements

* Windows (the `keyboard` library needs OS-level key injection; this is primarily tested on Windows, where osu! is most commonly played)
* [tosu](https://tosu.app) installed and running alongside osu!lazer

## Installation

```bash
git clone https://github.com/mvased727/osu-Skin-Shuffle.git
cd osu-miss-random-skin
pip install -r requirements.txt
```

(The script also auto-installs missing dependencies on first run, so a manual `pip install` is optional.)

## Usage

1. Start [tosu](https://tosu.app). It auto-detects a running osu! instance.
2. Launch **osu!lazer**.
3. Run the script:

```bash
python osu\\\\\\\_miss\\\\\\\_random\\\\\\\_skin.py
```

4. Play. Every Miss now triggers a random skin change.

> \\\\\\\*\\\\\\\*Note:\\\\\\\*\\\\\\\* If osu!lazer is running as administrator, run this script as administrator too — otherwise Windows will block the simulated keystrokes from reaching an elevated window.

## Configuration

Both constants are at the top of `osu\\\\\\\_miss\\\\\\\_random\\\\\\\_skin.py`:

```python
TOSU\\\\\\\_WS\\\\\\\_URL = "ws://127.0.0.1:24050/websocket/v2"
HOTKEY = "ctrl+shift+r"
```

Change `HOTKEY` if you rebind random skin to something else in osu!.

## Troubleshooting

* **Nothing happens on miss** — open `http://127.0.0.1:24050/json` in a browser while playing and confirm the miss count is really under `play.hits\\\\\\\["0"]` in your tosu version; adjust `get\\\\\\\_miss\\\\\\\_count()` if the path changed.
* **`keyboard` fails to install** — likely a Python-version compatibility issue. Try a stable Python release (3.10–3.12) or switch to the [`pynput`](https://pypi.org/project/pynput/) library.
* **Script connects but hotkey doesn't reach the game** — run the script as administrator if osu!lazer itself runs elevated.

## Disclaimer

This tool only reads gameplay state and sends a cosmetic hotkey (skin change) — it does not read or write any score-affecting data and is not a gameplay cheat. Use at your own discretion.
