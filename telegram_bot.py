import requests
import json
import os

from crous_checker import VILLES, get_logements

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

OFFSET_FILE = "telegram_offset.json"


def get_updates(offset):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    r = requests.get(url, params={"offset": offset, "timeout": 0})
    return r.json()


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    print("Telegram status:", r.status_code, r.text[:200])


def check_all_villes():
    lines = ["📋 État actuel des logements CROUS :\n"]
    total = 0
    for ville, url in VILLES.items():
        try:
            logements = get_logements(url)
        except Exception as e:
            lines.append(f"⚠️ {ville}: erreur ({e})")
            continue
        total += len(logements)
        if logements:
            lines.append(f"🏠 {ville}: {len(logements)} logement(s)")
            for l in logements[:5]:
                lines.append(f"   ➡️ {l['name']}\n   {l['url']}")
        else:
            lines.append(f"— {ville}: aucun")
    lines.append(f"\nTotal: {total} logement(s) sur {len(VILLES)} ville(s).")
    return "\n".join(lines)


def check_one_ville(name):
    match = next((v for v in VILLES if v.lower() == name.lower()), None)
    if not match:
        return f"❌ Ville inconnue: {name}\nVilles suivies: {', '.join(VILLES.keys())}"
    logements = get_logements(VILLES[match])
    if not logements:
        return f"— Aucun logement actuellement à {match}."
    msg = f"🏠 {len(logements)} logement(s) à {match} :\n\n"
    for l in logements:
        msg += f"➡️ {l['name']}\n{l['url']}\n\n"
    return msg


def main():
    offset = 0
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE) as f:
            offset = json.load(f).get("offset", 0)

    data = get_updates(offset)
    if not data.get("ok"):
        print("Telegram getUpdates error:", data)
        return

    updates = data.get("result", [])
    print(f"Got {len(updates)} update(s)")

    for update in updates:
        offset = update["update_id"] + 1
        text = update.get("message", {}).get("text", "").strip()
        if not text:
            continue

        print("Command received:", text)

        if text.lower() in ("/check", "/checkall"):
            send_telegram(check_all_villes())
        elif text.lower().startswith("/check "):
            send_telegram(check_one_ville(text[len("/check "):].strip()))
        elif text.lower() in ("/start", "/help"):
            send_telegram(
                "🤖 Commandes disponibles:\n"
                "/check — état de toutes les villes suivies\n"
                "/check <ville> — état d'une ville précise\n"
                f"Villes suivies: {', '.join(VILLES.keys())}"
            )

    with open(OFFSET_FILE, "w") as f:
        json.dump({"offset": offset}, f)


if __name__ == "__main__":
    main()
