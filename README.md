# 🏠 CROUS Housing Monitor for ENSAE Paris (Palaiseau)

An automated monitoring system that continuously checks the official CROUS housing website for new accommodations around **ENSAE Paris (Palaiseau)** and sends instant **Telegram notifications** whenever a new listing becomes available.

The entire project runs **100% in the cloud** using **GitHub Actions**, meaning **your computer can be completely turned off** while the monitoring continues.

---

## 🚀 Features

- ✅ Automatic CROUS monitoring
- ✅ Instant Telegram notifications
- ✅ Runs entirely on GitHub Actions
- ✅ No server or VM required
- ✅ Free to use
- ✅ Fully customizable search area
- ✅ Easy to deploy

---

# How it works

```
                 Every 15 minutes
                        │
                        ▼
              GitHub Actions Runner
                        │
                        ▼
              Execute Python Script
                        │
                        ▼
       Read CROUS Search Results Page
                        │
                        ▼
       Compare with previously seen listings
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
     No new listing         New listing found
            │                       │
            ▼                       ▼
         Finish            Telegram Notification
                                    │
                                    ▼
                            Notification on phone
```

---

# Tech Stack

- Python 3.12
- GitHub Actions
- BeautifulSoup
- Requests
- Telegram Bot API

---

# Project Structure

```
crous-alert-palaiseau/
│
├── crous_checker.py
├── seen.json
├── requirements.txt
├── README.md
│
└── .github
    └── workflows
        └── check.yml
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/crous-alert-palaiseau.git

cd crous-alert-palaiseau
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Telegram Bot Setup

## Create a Bot

Open Telegram.

Search for

```
@BotFather
```

Run

```
/newbot
```

Choose

- Bot Name
- Username

BotFather returns

```
123456789:AAxxxxxxxxxxxxxxxxxxxxxxxx
```

Save it as

```
TELEGRAM_TOKEN
```

---

## Get your Chat ID

Open your bot.

Click **Start**

Send

```
Hello
```

Open

```
https://api.telegram.org/botYOUR_TOKEN/getUpdates
```

Example

```json
{
    "chat": {
        "id": 8979746858
    }
}
```

Save

```
8979746858
```

as

```
TELEGRAM_CHAT_ID
```

---

# GitHub Configuration

Go to

```
Repository
    ↓
Settings
    ↓
Secrets and variables
    ↓
Actions
```

Create these Repository Secrets.

| Secret | Description |
|---------|-------------|
| TELEGRAM_TOKEN | Telegram Bot Token |
| TELEGRAM_CHAT_ID | Telegram Chat ID |

---

# GitHub Workflow

The project automatically runs using GitHub Actions.

Workflow location

```
.github/workflows/check.yml
```

It supports two triggers.

Automatic

```yaml
schedule:
```

Manual

```yaml
workflow_dispatch:
```

You can manually test the bot from

```
GitHub

↓

Actions

↓

CROUS Alert

↓

Run workflow
```

---

# Search Area

The current search monitors accommodations around

- Palaiseau
- Massy
- Saclay
- Orsay
- Gif-sur-Yvette
- Bures-sur-Yvette
- Les Ulis

The monitored area can easily be changed by replacing the CROUS search URL inside

```
crous_checker.py
```

---

# Notification Example

```
🏠 New CROUS Accommodation

Residence Example

420 €

https://trouverunlogement.lescrous.fr/...
```

---

# Running Locally

```bash
python crous_checker.py
```

---

# Running Automatically

Nothing to do.

GitHub executes the workflow automatically.

Even if

- your computer is OFF
- you're travelling
- your laptop has no Internet

the monitoring continues.

---

# GitHub Actions Scheduling

GitHub scheduled workflows are **best effort**.

This means

```
Every 15 minutes
```

does **not** always mean exactly every 15 minutes.

Example

Expected

```
10:00
10:15
10:30
10:45
```

Possible execution

```
10:03
10:19
10:36
10:52
```

Sometimes GitHub may delay workflows during periods of high load.

This is a GitHub limitation rather than a project issue.

---

# Improving Reliability

For more consistent execution intervals, the workflow can also be triggered externally using **cron-job.org** through the GitHub API.

Recommended architecture

```
cron-job.org
      │
      ▼
GitHub API
      │
      ▼
GitHub Actions
      │
      ▼
Python Checker
      │
      ▼
Telegram Notification
```

This removes most scheduling delays while remaining completely free.

---

# Future Improvements

- Multiple search areas
- Email notifications
- Discord notifications
- Docker image
- Better duplicate detection
- Web dashboard
- Unit tests

---

# License

MIT License.

---

# Author

**Yassine Zamit**

Industrial & Data Engineer

Incoming **Mastère Spécialisé Data Science** student at **ENSAE Paris (Institut Polytechnique de Paris)**

---
⭐ If you find this project useful, consider giving it a star!
