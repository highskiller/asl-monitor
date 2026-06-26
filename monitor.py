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
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(10000)

        # DIAGNOSTICA: elenca iframe presenti
        frames = page.frames
        print(f"=== NUMERO FRAME: {len(frames)} ===")
        for i, f in enumerate(frames):
            print(f"Frame {i}: {f.url}")

        # DIAGNOSTICA: elenca tutti gli input della pagina principale
        print("=== INPUT NELLA PAGINA ===")
        inputs = page.query_selector_all("input, textarea, button")
        for el in inputs[:30]:
            tag = el.evaluate("e => e.tagName")
            name = el.get_attribute("name")
            eid = el.get_attribute("id")
            ptext = el.get_attribute("placeholder")
            print(f"{tag} name={name} id={eid} placeholder={ptext}")

        # DIAGNOSTICA: cerca testo 'banca dati' nell'intera pagina e nei frame
        total = 0
        for f in frames:
            try:
                t = f.content().lower()
                c = t.count("banca dati")
                if c > 0:
                    print(f">>> Frame {f.url} contiene 'banca dati' x{c}")
                total += c
            except Exception as e:
                pass
        print(f"=== TOTALE occorrenze 'banca dati' in tutti i frame: {total} ===")

        browser.close()

if __name__ == "__main__":
    main()
