import os
import requests

# Récupération des secrets depuis l'environnement GitHub
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
AV_KEY = os.environ.get("ALPHA_VANTAGE_KEY")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_price(ticker):
    # Utilisation de l'API Alpha Vantage (Global Quote)
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={AV_KEY}"
    data = requests.get(url).json()
    return data["Global Quote"]["05. price"]

def update_notion(page_id, price):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": {"Prix": {"number": float(price)}}}
    requests.patch(url, headers=headers, json=payload)

# 1. On liste les lignes de la base
res = requests.post(f"https://api.notion.com/v1/databases/{DATABASE_ID}/query", headers=headers)
pages = res.json().get("results", [])

# 2. On met à jour chaque ligne
for page in pages:
    # On suppose que le Ticker est dans la colonne titre "Name"
    ticker = page["properties"]["Name"]["title"][0]["plain_text"]
    try:
        current_price = get_price(ticker)
        update_notion(page["id"], current_price)
        print(f"Succès : {ticker} mis à jour à {current_price}")
    except Exception as e:
        print(f"Erreur sur {ticker} : {e}")
