import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Endpoint elenco repertori/concorsi ASL Bari
URL = "https://www.sanita.puglia.it/aol/listConcorso"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def get_rendered_text():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        # attende caricamento iniziale dei dati
        page.wait_for_timeout(8000)

        # Prova a compilare il campo "Oggetto" con "banca dati" e premere Ricerca
        try:
            # cerca un campo input di testo per l'oggetto
            page.fill("input[name='oggetto'], input#oggetto, textarea[name='oggetto']", "banca dati")
        except Exception as e:
            print(f"(campo oggetto non trovato: {e})")

        try:
            # clicca il pulsante Ricerca
            page.click("text=Ricerca", timeout=5000)
        except Exception as e:
            print(f"(pulsante Ricerca non cliccato: {e})")

        page.wait_for_timeout(8000)
        text = page.content().lower()
        browser.close()
        return text

def main():
    print("Controllo albo concorsi ASL Bari...")
    try:
        content = get_rendered_text()
    except Exception as e:
        print(f"Errore Playwright: {e}")
        return

    has_banca = "banca dati" in content
    has_scritta = "prova scritta" in content or "scritta" in content
    has_1000 = "1000 posti" in content or "1.000 posti" in content

    print(f"banca dati: {has_banca} | scritta: {has_scritta} | 1000posti: {has_1000}")
    # debug: stampa quante volte appare "banca dati"
    print(f"occorrenze 'banca dati': {content.count('banca dati')}")

    if has_banca and has_scritta:
        send_telegram(
            "🚨🚨 POSSIBILE BANCA DATI PROVA SCRITTA! 🚨🚨\n\n"
            "Nell'albo concorsi ASL Bari compare 'banca dati' + 'prova scritta'.\n\n"
            "👉 Controlla e scarica subito:\n"
            "https://www.sanita.puglia.it/aol/listConcorso"
        )
        print(">>> NOTIFICA INVIATA!")
    else:
        print("Nessuna novita rilevante.")

if __name__ == "__main__":
    main()
