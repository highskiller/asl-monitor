import requests
import hashlib
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL_DA_MONITORARE = "https://www.sanita.puglia.it/web/asl-bari/concorsi-e-avvisi"
KEYWORD = "infermier"  # parola chiave da cercare nella pagina

def get_page_content():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL_DA_MONITORARE, headers=headers, timeout=15)
    return response.text.lower()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def main():
    print("Controllo pagina ASL Bari...")
    content = get_page_content()

    # Cerca la keyword "banca dati" nella pagina
    if KEYWORD in content:
        # Controlla se contiene riferimento alla prova scritta
        if "scritta" in content or "27 giugno" in content or "3000" in content:
            send_telegram(
                "🚨 ATTENZIONE! La banca dati della prova scritta sembra essere apparsa sul sito ASL Bari!\n\n"
                "👉 Controlla subito: https://www.sanita.puglia.it/web/asl-bari/concorsi-e-avvisi"
            )
            print("Notifica inviata!")
        else:
            print("Trovata keyword 'banca dati' ma probabilmente è quella della preselezione già nota.")
    else:
        print("Nessuna novità sulla banca dati scritta.")

if __name__ == "__main__":
    main()
