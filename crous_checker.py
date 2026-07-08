import requests
import json
import os
from bs4 import BeautifulSoup


URL = "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.19174_48.7300913_2.2668688_48.700804&locationName=Palaiseau+%2891120%29"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

STATE_FILE = "seen.json"



def get_logements():

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    r = requests.get(
        URL,
        headers=headers
    )

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )

    logements = []

    cards = soup.find_all(
        "a",
        href=True
    )


    for c in cards:

        href = c["href"]

        if "/accommodations/" in href:

            title = c.text.strip()

            logements.append(
                {
                    "name": title,
                    "url":
                    "https://trouverunlogement.lescrous.fr"
                    + href
                }
            )


    return logements



def send_telegram(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_TOKEN}/sendMessage"
    )

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )



def main():

    logements = get_logements()


    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE
        ) as f:
            old = json.load(f)

    else:
        old = []


    new = []


    for logement in logements:

        if logement["url"] not in old:
            new.append(logement)


    if new:

        msg = "🏠 Nouveau logement CROUS Palaiseau !\n\n"

        for l in new:

            msg += (
                f"➡️ {l['name']}\n"
                f"{l['url']}\n\n"
            )


        send_telegram(msg)



    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            [
                l["url"]
                for l in logements
            ],
            f
        )



if __name__ == "__main__":
    main()
