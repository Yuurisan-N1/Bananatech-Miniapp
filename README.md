<div align="center">

<img width="100%" alt="header" src="https://capsule-render.vercel.app/api?type=waving&height=210&text=Banana%20Tech%20Bot&fontAlign=50&fontAlignY=36&fontSize=56&desc=Auto%20Tasks%20%7C%20Proxy%20Support%20%7C%20Multi-Account&descAlign=50&descAlignY=58"/>

<img alt="typing" src="https://readme-typing-svg.demolab.com?font=Inter&size=18&duration=3000&pause=650&center=true&vCenter=true&width=900&lines=Auto+Complete+All+Tasks+%7C+Earn+Points+Per+Task;Auto+Filter+Done+Tasks+%7C+Only+Process+Pending+Ones;Proxy+Support+%7C+One+Proxy+Per+Account;Multi-Account+%7C+Sequential+Processing+Per+Cycle"/>

<p>
  <img alt="python" src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white"/>
  <img alt="platform" src="https://img.shields.io/badge/Platform-Banana%20Tech%20Miniapp-111111"/>
  <img alt="multi-account" src="https://img.shields.io/badge/Multi--Account-Supported-111111"/>
  <img alt="proxy" src="https://img.shields.io/badge/Proxy-Supported-111111"/>
  <img alt="author" src="https://img.shields.io/badge/by-Yuurisandesu-111111"/>
</p>

<p>
  <b>Banana Tech Bot</b> is a full automation bot for the Banana Tech Telegram Miniapp.<br/>
  It handles the complete daily cycle: authenticating each account to obtain a session token, fetching the full task list and filtering out already-completed ones, then starting and claiming every pending task to collect point rewards, all running across multiple accounts with proxy support and a live countdown between cycles.<br/>
  Built and distributed by <b>Yuurisandesu</b>.
</p>

</div>

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Features](#features)
- [File Structure](#file-structure)
- [Disclaimer](#disclaimer)

---

## Requirements

- Python `3.12+`
- Git

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Yuurisan-N1/Bananatech-Miniapp.git
cd Bananatech-Miniapp
```

**Install dependencies:**

```bash
pip install requests python-dotenv yuurisan
```

---

## Configuration

### 1. Accounts (data.txt)

Fill `data.txt` with Telegram WebApp `initData` for each account, one per line:

```
user=%7B%22id%22...&hash=abc123
user=%7B%22id%22...&hash=def456
```

> `initData` can be obtained from the browser DevTools when opening Banana Tech on Telegram Web.

### 2. Proxy (proxy.txt) - Optional

Fill `proxy.txt` with proxies, one per line. Proxies are assigned to accounts by index (first proxy to first account, second proxy to second account, and so on). If the number of proxies is fewer than the number of accounts, proxies wrap around cyclically. If `proxy.txt` is missing or empty, the bot runs without a proxy.

```
http://user:pass@ip:port
http://user:pass@ip:port
```

Supported format: `http://user:pass@host:port`

### 3. Bot Settings (config.json)

`sleep_seconds` controls how many seconds the bot waits between cycles. If `config.json` is missing, the bot falls back to a default of `3600` seconds.

```json
{
  "settings": {
    "sleep_seconds": 3600
  }
}
```

---

## Running the Bot

```bash
python bot.py
```

Press `Ctrl+C` at any time to stop the bot cleanly.

---

## Features

### Auto Login
The bot authenticates each account by posting the `initData` string to the Banana Tech auth endpoint to obtain a Bearer access token. If the token is not returned or the request fails, the account is skipped for that cycle without stopping the rest. A success message is logged when the token is obtained successfully.

### Auto Tasks
The bot fetches the full task list from the server and splits them into two groups: pending tasks where `is_completed` is false and already done tasks where `is_completed` is true. The total count of each group is logged. If all tasks are already completed, the account is skipped immediately. For each pending task, the bot sends a start request with the task ID and its action URL as proof data, then logs the task title, resulting status, and points awarded. Tasks that return a COMPLETED status are logged as successful. Tasks that return any other status are logged with that status. Failed requests are logged individually without stopping the rest. A 1 second delay is applied between each task to avoid rate limiting.

### Completed Task Filter
Before processing, the bot separates tasks that are already marked as completed on the server. Only tasks with `is_completed` set to false are submitted. This prevents duplicate submissions and keeps each cycle efficient even when most tasks are already done.

### Proxy Support
Each account can be assigned its own proxy via `proxy.txt`. If a proxy is configured for the current account, it is shown in masked form before processing begins. Proxy assignment uses a round-robin fallback if there are fewer proxies than accounts. If no proxy is set for an account, the bot logs that it is running without a proxy for that account.

### Multi Account
All accounts in `data.txt` are processed sequentially within every cycle. Account number is logged at the start of each account. A blank line separates each account output in the terminal for readability.

### Auto Countdown
After all accounts complete a cycle, the bot logs that all accounts have been processed and displays a live `HH:MM:SS` countdown in the terminal until the next cycle starts, then re-shows the banner before beginning again.

---

## File Structure

```text
Bananatech-Miniapp/
├── bot.py          # Main bot, full daily cycle automation
├── config.json     # Sleep duration between cycles
├── data.txt        # Account initData, one per line
├── proxy.txt       # Proxies, one per line (optional)
├── LICENSE         # License file
└── utils/
    ├── banner.py   # Banner display on startup
    └── __init__.py
```

---

## Disclaimer

This tool is built for educational and technical exploration purposes. Use it wisely and at your own responsibility.

---

<div align="center">
<img width="100%" alt="footer" src="https://capsule-render.vercel.app/api?type=waving&height=120&section=footer"/>
</div>