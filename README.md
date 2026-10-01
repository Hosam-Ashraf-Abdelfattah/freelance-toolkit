# Freelance Toolkit — Contract Generator & Pricing Bot

> 🇪🇬 [النسخة العربية](README.ar.md) · 📖 [Full documentation](docs/DOCUMENTATION.md)

A Python toolkit for freelance developers that automates two time-consuming jobs:

1. **Contract Generator** – turns an Excel sheet into professional **bilingual (Arabic / English) PDF contracts** with correct RTL rendering, Egyptian-law clauses, a SHA-256 integrity hash and a QR code.
2. **Pricing Bot** – a **Telegram bot** (text + voice) that scrapes Upwork, Freelancer and Fiverr for market rates, converts USD → EGP and replies to the client with a text summary and a voice message.

<p align="center">
  <img src="docs/images/contract_preview.png" alt="Generated contract preview" width="420">
</p>

## Features

| Module | What it does |
|---|---|
| `contract_generator.py` | Reads contracts + milestones from Excel, builds HTML/CSS, renders PDF with WeasyPrint |
| `excel_generator.py` | Creates a ready-to-edit sample Excel file (3 contracts, milestones) |
| `telegram_bot.py` | FAQ bot with voice-to-text (Google Speech) and text-to-speech (gTTS) |
| `calculate_project_pricing.py` | Selenium scraper + price extractor + live USD→EGP rate |
| `telegram_makes_pricing.py` | Combines the bot and the scraper into one app |

## Quick start

```bash
git clone https://github.com/Hosam-Ashraf-Abdelfattah/freelance-toolkit.git
cd freelance-toolkit
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 1) Generate contracts

```bash
python excel_generator.py        # creates contracts_data.xlsx (sample data)
python contract_generator.py     # creates PDFs in generated_contracts/
```

### 2) Run the pricing bot

```bash
cp .env.example .env             # then put your TELEGRAM_BOT_TOKEN inside
python telegram_makes_pricing.py
```

Then message your bot, e.g. `price of python web scraping`.

## System requirements

- Python 3.10 – 3.12
- **WeasyPrint** system libraries (Pango) – see the [WeasyPrint install guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)
- **FFmpeg** (for voice messages)
- **Google Chrome** (for the scraper)

## Project structure

```
freelance-toolkit/
├── contract_generator.py
├── excel_generator.py
├── telegram_bot.py
├── calculate_project_pricing.py
├── telegram_makes_pricing.py
├── requirements.txt
├── .env.example
├── docs/                 # full documentation (EN / AR) + images
└── examples/             # sample Excel, sample PDFs, sample pricing JSON
```

## Important notes

- **Not legal advice.** The contract clauses are a starting template. Have a qualified lawyer review them before real use.
- **Signing link is a placeholder.** `https://contractsign.app` is a stand-in domain; this repo does not include a signing backend.
- **Scraping:** automated access may violate the terms of the platforms you scrape, and results depend on page layout and anti-bot protection (Upwork often returns nothing). Use responsibly and treat numbers as rough estimates.
- **Secrets:** the bot token is read from `.env`. Never commit it.

## License

MIT — see [LICENSE](LICENSE).
