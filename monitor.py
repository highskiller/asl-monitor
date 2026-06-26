import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.sanita.puglia.it/aol/listConcorso"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(8000)

        print(f"URL attuale: {page.url}")

        # Stampa il testo di tutti i bottoni (per trovare ASL Bari)
        print("=== TESTO DEI BOTTONI ===")
        buttons = page.query_selector_all("button, a, div[onclick], span[onclick]")
        for i, el in enumerate(buttons[:40]):
            try:
                txt = (el.inner_text() or "").strip()
                if txt:
                    print(f"[{i}] '{txt}'")
            except Exception:
                pass

        # Prova a cliccare su ASL Bari
        print("=== TENTATIVO CLICK ASL BARI ===")
        clicked = False
        for sel in ["text=ASL Bari", "text=Bari", "text=aslbari"]:
            try:
                page.click(sel, timeout=4000)
                print(f"Cliccato con selettore: {sel}")
                clicked = True
                break
            except Exception as e:
                print(f"  fallito {sel}")

        if clicked:
            page.wait_for_timeout(8000)
            print(f"Nuovo URL: {page.url}")
            text = page.content().lower()
            print(f"occorrenze 'banca dati': {text.count('banca dati')}")
            print(f"occorrenze 'concorso': {text.count('concorso')}")
            print(f"occorrenze 'infermiere': {text.count('infermiere')}")

        browser.close()

if __name__ == "__main__":
    main()
