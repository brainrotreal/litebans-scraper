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
def get_bans(request: Request, limit: int = 10):
    limit = max(1, min(limit, 100))

    r = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0"
    }, timeout=15)

    soup = BeautifulSoup(r.text, "html.parser")

    bans = []

    for tr in soup.select("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.select("td")]

        if len(cells) != 5:
            continue

        ban = {
            "player": cells[0],
            "banned_by": cells[1],
            "reason": cells[2],
            "date": cells[3],
            "expires": cells[4],
            "unbanned": "Unbanned by" in cells[4],
            "permanent": "Permanent" in cells[4],
        }

        bans.append(ban)

    return {
        "count": len(bans[:limit]),
        "total_found": len(bans),
        "limit": limit,
        "bans": bans[:limit]
    }