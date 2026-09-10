# osu!SkinShuffle
<img width="2720" height="1200" alt="skin_shuffle_hexagon_rounded" src="https://github.com/user-attachments/assets/a09169c4-2488-4d70-beb5-7a90ba75d1ac" />

[![Download](https://img.shields.io/github/v/release/mvased727/osu-Skin-Shuffle?label=Download&style=for-the-badge)](https://github.com/mvased727/osu-Skin-Shuffle/releases/latest)


[Download tosu]([https://tosu.app](https://github.com/tosuapp/tosu))


Automatically triggers osu!'s **random skin** hotkey (`Ctrl+Shift+R`) every time you get a **Miss** while playing **osu!lazer** (or stable). 100s and 50s do not trigger it — only actual misses.

It works by reading live gameplay data from [tosu](https://tosu.app), a memory-reading tool for osu!, over its WebSocket API, and sending the hotkey via the [`keyboard`](https://pypi.org/project/keyboard/) library.

## How it works

1. [tosu](https://tosu.app) reads osu!'s game memory and exposes real-time gameplay state (combo, hit counts, etc.) over a local WebSocket server (`ws://127.0.0.1:24050/websocket/v2`).
2. This script connects to that WebSocket and watches the miss counter (`play.hits["0"]`).
3. Whenever the miss counter increases during active gameplay, it sends `Ctrl+Shift+R`.
4. The counter resets whenever you leave gameplay (menu, results screen, retry), so starting a new map is never mistaken for a miss.

## Installation

Download the latest version from the [Releases](https://github.com/mvased727/osu-Skin-Shuffle/releases/latest) page and extract the ZIP file.

## Usage

1. Start [tosu](https://tosu.app). It auto-detects a running osu! instance.
2. Launch **osu!lazer**.
3. Run the osu-skin-shuffle.exe.
4. That's it. Every miss now triggers a random skin change.

> Note: If osu!lazer is running as administrator, run this script as administrator too — otherwise Windows will block the simulated keystrokes from reaching an elevated window.

## Troubleshooting

* **Script connects but hotkey doesn't reach the game** — run the script as administrator if osu!lazer itself runs elevated.

## Disclaimer

This tool only reads gameplay state and sends a cosmetic hotkey (skin change) — it does not read or write any score-affecting data and is not a gameplay cheat. Use at your own discretion.
