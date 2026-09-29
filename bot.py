import requests
import json
import time
import sys
import signal
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.banner import show_banner

load_dotenv()

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

MY_PROJECT = "Banana Tech Miniapp"

def log_green(msg):
    print(f"{GREEN}{BOLD}{msg}{RESET}")

def log_yellow(msg):
    print(f"{YELLOW}{BOLD}{msg}{RESET}")

def log_red(msg):
    print(f"{RED}{BOLD}{msg}{RESET}")

def signal_handler(sig, frame):
    print()
    log_red("Script stopped by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_data():
    with open("data.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies():
    if not os.path.exists("proxy.txt"):
        return []
    with open("proxy.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def get_proxy_dict(proxy_str):
    if not proxy_str:
        return None
    return {"http": proxy_str, "https": proxy_str}

def mask_proxy(proxy_str):
    try:
        parts = proxy_str.split("@")
        if len(parts) == 2:
            credentials = parts[0]
            host_port = parts[1]
            ip_port = host_port.split(":")
            ip = ip_port[0]
            port = ip_port[1] if len(ip_port) > 1 else ""
            ip_parts = ip.split(".")
            if len(ip_parts) == 4:
                masked_ip = f"{ip_parts[0]}*****{ip_parts[3]}"
            else:
                masked_ip = ip[:2] + "*****"
            scheme = credentials.split("://")[0] if "://" in credentials else "http"
            return f"http://user:pass@{masked_ip}:{port}"
        else:
            ip = proxy_str.split(":")[0] if ":" in proxy_str else proxy_str
            ip_parts = ip.split(".")
            if len(ip_parts) == 4:
                masked_ip = f"{ip_parts[0]}*****{ip_parts[3]}"
            else:
                masked_ip = ip[:2] + "*****"
            return f"http://user:pass@{masked_ip}:****"
    except Exception:
        return "http://user:pass@*****:****"

HEADERS_BASE = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://giveaway-app.bananatech.space",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://giveaway-app.bananatech.space/",
    "sec-ch-ua": '"Microsoft Edge";v="154", "Not A(Brand";v="99", "Microsoft Edge WebView2";v="154", "Chromium";v="154"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 Edg/154.0.0.0",
}

def get_token(init_data, proxy_dict):
    url = "https://giveaway.bananatech.space/auth/telegram/auth"
    headers = {**HEADERS_BASE, "content-type": "application/json"}
    payload = {"init_data": init_data}
    resp = requests.post(url, headers=headers, json=payload, proxies=proxy_dict, timeout=30)
    resp.raise_for_status()
    return resp.json()

def get_tasks(token, proxy_dict):
    url = "https://giveaway.bananatech.space/giveaway/tasks"
    headers = {**HEADERS_BASE, "authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, proxies=proxy_dict, timeout=30)
    resp.raise_for_status()
    return resp.json()

def start_task(token, task_id, proof_data, proxy_dict):
    url = "https://giveaway.bananatech.space/giveaway/tasks/start"
    headers = {**HEADERS_BASE, "content-type": "application/json", "authorization": f"Bearer {token}"}
    payload = {"task_id": task_id, "proof_data": proof_data}
    resp = requests.post(url, headers=headers, json=payload, proxies=proxy_dict, timeout=30)
    resp.raise_for_status()
    return resp.json()

def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        timer = f"{h:02d}:{m:02d}:{s:02d}"
        print(f"{YELLOW}{BOLD}Next cycle starts in {timer}{RESET}", end="\r", flush=True)
        time.sleep(1)
    print(" " * 60, end="\r")

def process_account(init_data, proxy_dict, account_index):
    log_yellow(f"Processing account number {account_index + 1}.")

    if proxy_dict:
        raw_proxy = list(proxy_dict.values())[0]
        log_yellow(f"Using proxy {mask_proxy(raw_proxy)}.")
    else:
        log_yellow("Running without proxy for this account.")

    try:
        token_data = get_token(init_data, proxy_dict)
        access_token = token_data.get("access_token")
        if not access_token:
            log_red("Failed to retrieve access token for this account.")
            return
        log_green("Authentication successful, token obtained.")
    except Exception:
        log_red("Authentication request failed for this account.")
        return

    try:
        tasks_data = get_tasks(access_token, proxy_dict)
        items = tasks_data.get("items", [])
        total = tasks_data.get("total", 0)
        log_green(f"Fetched {total} total tasks from server.")
    except Exception:
        log_red("Failed to fetch task list for this account.")
        return

    pending = [t for t in items if not t.get("is_completed")]
    already_done = [t for t in items if t.get("is_completed")]

    log_yellow(f"Found {len(pending)} uncompleted tasks and {len(already_done)} already done.")

    if not pending:
        log_green("All tasks already completed for this account.")
        return

    for task in pending:
        task_id = task.get("id")
        title = task.get("title", {}).get("en", f"Task {task_id}")
        reward = task.get("reward_points", 0)
        action_url = task.get("action_url", "https://bananatech.space")

        try:
            result = start_task(access_token, task_id, action_url, proxy_dict)
            status = result.get("status", "UNKNOWN")
            points = result.get("points_awarded", 0)
            if status == "COMPLETED":
                log_green(f"Task completed successfully: {title}, earned {points} points.")
            else:
                log_yellow(f"Task submitted with status {status}: {title}.")
        except Exception:
            log_red(f"Failed to claim task: {title}, reward was {reward} points.")

        time.sleep(1)

def main():
    show_banner(MY_PROJECT)

    config = load_config()
    sleep_seconds = config.get("settings", {}).get("sleep_seconds", 3600)

    data_list = load_data()
    proxy_list = load_proxies()

    while True:
        for idx, init_data in enumerate(data_list):
            if idx > 0:
                print()

            proxy_str = None
            if proxy_list:
                proxy_str = proxy_list[idx % len(proxy_list)]

            proxy_dict = get_proxy_dict(proxy_str)
            process_account(init_data, proxy_dict, idx)

        log_yellow(f"All accounts processed")
        countdown(sleep_seconds)
        show_banner(MY_PROJECT)

if __name__ == "__main__":
    main()
