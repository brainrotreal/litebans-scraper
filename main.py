from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import requests
from bs4 import BeautifulSoup

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

URL = "https://stoneworks.gg/bans/bans.php"

@app.get("/bans")
@limiter.limit("3/second")
def get_bans(request: Request):
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

@app.get("/test")
def test(request: Request):
    return {"message": "Hello, World!"}

@app.get("/debug_redirect")
def debug_redirect(request: Request):
    r = requests.get(
        "https://stoneworks.gg/bans/bans.php",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
        allow_redirects=False
    )

    return {
        "status": r.status_code,
        "location": r.headers.get("Location"),
        "text": r.text[:500]
    }