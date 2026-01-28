import requests
import json
from datetime import datetime, timedelta
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # your chat or group id
EVENTS_FILE = "ctf_events.json"

def send_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def send_reminders():
    now = datetime.utcnow()
    next24h = now + timedelta(hours=24)

    with open(EVENTS_FILE) as f:
        events = json.load(f)

    for e in events:
        start = datetime.strptime(e["start"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        if now <= start <= next24h:
            msg = f"🚨 *CTF Reminder*\n🏴 {e['title']}\n🕒 {start} UTC\n🔗 {e['ctftime_url']}"
            send_message(msg)

def send_week_list():
    with open(EVENTS_FILE) as f:
        events = json.load(f)
    msg = "📅 *CTFs This Week*\n\n"
    for e in events:
        start = datetime.strptime(e["start"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        msg += f"🏴 {e['title']}\n🕒 {start} UTC\n🔗 {e['ctftime_url']}\n\n"
    send_message(msg)

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "week":
        send_week_list()
    else:
        send_reminders()

if __name__ == "__main__":
    main()
