import urllib.request
import os

URL = "https://livepocket.jp/e/20261231labsync"
NTFY_URL = "https://ntfy.sh/ugggggggg"
STATE_FILE = "last_status.txt"

def get_page():
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")

def notify(message):
    req = urllib.request.Request(
        NTFY_URL,
        data=message.encode("utf-8"),
        headers={
            "Title": "LivePocket 販売開始",
            "Priority": "high"
        },
        method="POST"
    )
    urllib.request.urlopen(req, timeout=30)

page = get_page()

print("取得したページの文字数:", len(page))
print("取得したページの先頭:", repr(page[:500]))

if "販売中" in page:
    status = "販売中"
elif "予定販売枚数終了" in page or "販売枚数終了" in page:
    status = "販売終了"
else:
    status = "不明"

print("現在の判定:", status)

old_status = None
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old_status = f.read().strip()

print("前回の判定:", old_status)

if old_status == "販売終了" and status == "販売中":
    notify("LivePocketのチケットが販売中になりました！")
    print("通知を送信しました")

with open(STATE_FILE, "w", encoding="utf-8") as f:
    f.write(status)
