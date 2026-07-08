import requests
import json
import os
from bs4 import BeautifulSoup

VILLES = {
    "Palaiseau": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.19174_48.7300913_2.2668688_48.700804&locationName=Palaiseau+%2891120%29",
    "Massy": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.2350_48.7450_2.3100_48.7150&locationName=Massy+%2891300%29",
    "Orsay": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.1350_48.7140_2.2100_48.6840&locationName=Orsay+%2891400%29",
    "Gif-sur-Yvette": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.0958688_48.7184219_2.1725309_48.6740284&locationName=Gif-sur-Yvette+%2891190%29",
    "Bures-sur-Yvette": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.1414182_48.7070448_2.1762154_48.675628&locationName=Bures-sur-Yvette+%2891440%29",
    "Antony": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.274543_48.7721397_2.3206998_48.7293024&locationName=Antony+%2892160%29",
    "Cachan": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.3186757_48.8015527_2.3449625_48.7812228&locationName=Cachan+%2894230%29",
    "Sceaux": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.2782666_48.7854458_2.3142729_48.7665986&locationName=Sceaux+%2892330%29",
    "Évry": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.4130316_48.6485333_2.4705092_48.6109217&locationName=%C3%89vry+%2891000%29",
    "Versailles": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.0699384_48.82861_2.1683504_48.7792297&locationName=Versailles+%2878000%29",
    "Paris": "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.224122_48.902156_2.4697602_48.8155755&locationName=Paris",
    "Ile-de-France" : "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=1.4462445_49.241431_3.5592208_48.1201456&locationName=%C3%8Ele-de-France",
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
        try:
            logements = get_logements(url)
        except Exception as e:
            print(f"[{ville}] ERROR fetching: {e}")
            new_state[ville] = old_state.get(ville, [])  # keep old state, don't wipe it
            continue

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
