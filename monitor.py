import os
from playwright.sync_api import sync_playwright
import urllib.request

URL = "https://livepocket.jp/e/20261231labsync"
NTFY_URL = "https://ntfy.sh/ugggggggg"
STATE_FILE = "last_status.txt"

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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle", timeout=60000)

    text = page.locator("body").inner_text()

    print("取得したページの文字数:", len(text))
    print("取得したページの先頭:", repr(text[:500]))

    browser.close()

if "販売中" in text:
    status = "販売中"
elif "予定販売枚数終了" in text or "販売枚数終了" in text:
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
