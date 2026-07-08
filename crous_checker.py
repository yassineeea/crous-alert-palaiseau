import requests
import json
import os
from bs4 import BeautifulSoup

VILLES = {
    "Palaiseau": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.19174_48.7300913_2.2668688_48.700804&locationName=Palaiseau+%2891120%29",
    "Massy":     "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.2350_48.7450_2.3100_48.7150&locationName=Massy+%2891300%29",
    "Orsay":     "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.1350_48.7140_2.2100_48.6840&locationName=Orsay+%2891400%29",
    "Grenoble":     "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=6.1360042_49.1487955_6.256451_49.0608244&locationName=Metz",
    "Paris":  "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.224122_48.902156_2.4697602_48.8155755&locationName=Paris",
}

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

STATE_FILE = "seen.json"


def get_logements(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    logements = []
    for c in soup.find_all("a", href=True):
        href = c["href"]
        if "/accommodations/" in href:
            logements.append({
                "name": c.text.strip(),
                "url": "https://trouverunlogement.lescrous.fr" + href
            })
    return logements


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    print("Telegram status:", r.status_code, r.text[:200])


def main():
    old_state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            old_state = json.load(f)

    new_state = {}

    for ville, url in VILLES.items():
        logements = get_logements(url)
        print(f"[{ville}] Found {len(logements)} logement(s)")

        old_urls = old_state.get(ville, [])
        new = [l for l in logements if l["url"] not in old_urls]
        print(f"[{ville}] {len(new)} new logement(s) since last run")

        if new:
            msg = f"🏠 Nouveau logement CROUS à {ville} !\n\n"
            for l in new:
                msg += f"➡️ {l['name']}\n{l['url']}\n\n"
            send_telegram(msg)

        new_state[ville] = [l["url"] for l in logements]

    with open(STATE_FILE, "w") as f:
        json.dump(new_state, f)


if __name__ == "__main__":
    main()
