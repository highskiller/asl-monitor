import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.sanita.puglia.it/aol/listConcorso"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(8000)

        # 1) seleziona ASL Bari
        page.click("text=ASL Bari", timeout=10000)
        page.wait_for_timeout(8000)

        # 2) compila il campo Oggetto con "banca dati"
        filled = False
        try:
            campo = page.locator("mat-form-field:has-text('Oggetto') input").first
            campo.fill("banca dati", timeout=5000)
            filled = True
        except Exception:
            for i in range(8):
                try:
                    page.fill(f"#mat-input-{i}", "banca dati", timeout=2000)
                    filled = True
                    break
                except Exception:
                    pass

        # 3) clicca Ricerca
        if filled:
            for sel in ["button:has-text('Ricerca')", "text=Ricerca"]:
                try:
                    page.click(sel, timeout=3000)
                    break
                except Exception:
                    pass
            page.wait_for_timeout(8000)

        text = page.content().lower()
        browser.close()

    # Conteggi
    n_banca = text.count("banca dati")
    n_scritta = text.count("scritta")
    n_inf = text.count("infermiere")
    print(f"banca dati: {n_banca} | scritta: {n_scritta} | infermiere: {n_inf}")

    # SEGNALE: appare la parola "scritta" insieme a "banca dati" e "infermiere"
    # (la banca dati della preselettiva NON contiene "scritta")
    if n_banca > 0 and n_scritta > 0 and n_inf > 0:
        send_telegram(
            "🚨🚨 BANCA DATI PROVA SCRITTA INFERMIERI PUBBLICATA! 🚨🚨\n\n"
            "Nell'albo ASL Bari e' comparso un nuovo elemento 'banca dati' "
            "collegato alla PROVA SCRITTA del concorso infermieri.\n\n"
            "👉 Vai subito su:\n"
            "https://www.sanita.puglia.it/aol/listConcorso\n"
            "(seleziona ASL Bari, cerca 'banca dati')"
        )
        print(">>> NOTIFICA INVIATA!")
    else:
        print("Nessuna novita: banca dati scritta non ancora pubblicata.")

if __name__ == "__main__":
    main()
