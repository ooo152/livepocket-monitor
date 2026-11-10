import hashlib
import os
import urllib.request

URL = "https://livepocket.jp/e/20261231labsync"
STATE_FILE = "last_hash.txt"
NTFY_URL = "https://ntfy.sh/uggggggg"


def get_page():
    req = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def notify(message):
    req = urllib.request.Request(
        NTFY_URL,
        data=message.encode("utf-8"),
        headers={
            "Title": "LivePocketに変更がありました",
            "Priority": "high"
        },
        method="POST"
    )
    urllib.request.urlopen(req, timeout=30)


page = get_page()
new_hash = hashlib.sha256(page).hexdigest()

old_hash = None
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        old_hash = f.read().strip()

if old_hash is not None and old_hash != new_hash:
    notify("LivePocketのページに変更がありました。確認してください。")

with open(STATE_FILE, "w") as f:
    f.write(new_hash)
