import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Pagina albo pretorio ASL Bari - elenco concorsi (contenuto via JavaScript)
URL = "https://www.sanita.puglia.it/aol/listConcorso"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def get_rendered_text():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle", timeout=90000)
        # aspetta il caricamento dei dati dinamici
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

    # Cerca un repertorio "banca dati" legato alla prova SCRITTA del concorso 1000 posti
    has_banca = "banca dati" in content
    # segnali specifici della SCRITTA (non preselettiva)
    has_scritta = "prova scritta" in content or "scritta" in content
    # segnali del concorso 1000 infermieri
    has_1000 = "1000 posti" in content or "1.000 posti" in content or "mille" in content

    print(f"banca dati: {has_banca} | scritta: {has_scritta} | 1000: {has_1000}")

    # Notifica FORTE: banca dati + scritta presenti insieme
    if has_banca and has_scritta:
        send_telegram(
            "🚨🚨 POSSIBILE BANCA DATI PROVA SCRITTA! 🚨🚨\n\n"
            "Nell'albo concorsi ASL Bari compare un riferimento a 'banca dati' + 'prova scritta'.\n\n"
            "👉 Controlla e scarica subito:\n"
            "https://www.sanita.puglia.it/web/asl-bari/concorsi-e-avvisi"
        )
        print(">>> NOTIFICA FORTE INVIATA!")
    else:
        print("Nessuna novita rilevante sulla banca dati scritta.")

if __name__ == "__main__":
    main()
