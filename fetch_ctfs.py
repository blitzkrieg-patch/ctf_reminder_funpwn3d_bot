import requests
import json
from datetime import datetime, timedelta

CTFTIME_API = "https://ctftime.org/api/v1/events/"

def fetch_week_ctfs():
    res = requests.get(CTFTIME_API)
    events = res.json()
    now = datetime.utcnow()
    end_week = now + timedelta(days=7)

    week_events = []
    for e in events:
        start = datetime.strptime(e["start"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        if now <= start <= end_week:
            week_events.append({
                "id": e.get("id") or e.get("title"),
                "title": e["title"],
                "start": e["start"],
                "ctftime_url": e["ctftime_url"]
            })

    with open("ctf_events.json", "w") as f:
        json.dump(week_events, f, indent=2)
    print(f"Saved {len(week_events)} events for the week")

if __name__ == "__main__":
    fetch_week_ctfs()
