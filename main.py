from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

URL = "https://stoneworks.gg/bans/bans.php"

@app.get("/bans")
def get_bans():
    r = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0"
    }, timeout=15)

    soup = BeautifulSoup(r.text, "html.parser")

    # debug first: return visible text
    rows = []

    for tr in soup.select("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.select("td, th")]
        if cells:
            rows.append(cells)

    return {
        "count": len(rows),
        "rows": rows[:100]
    }