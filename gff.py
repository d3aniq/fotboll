import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

BASE_URL = "https://www.gbgfotboll.se/api/matches-today/games/?showReferees=true&associationId=7&date="

async def fetch_json(session, date_str):
    url = BASE_URL + date_str
    print(f"Hämtar {url}")

    try:
        async with session.get(url, timeout=20) as resp:
            return await resp.json()
    except Exception as e:
        print(f"Fel vid hämtning av {date_str}: {e}")
        return None


async def fetch_range_merge(date_from, date_to):
    start = datetime.strptime(date_from, "%Y-%m-%d")
    end = datetime.strptime(date_to, "%Y-%m-%d")

    all_data = {}

    async with aiohttp.ClientSession() as session:
        current = start
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            data = await fetch_json(session, date_str)

            if data is not None:
                all_data[date_str] = data

            current += timedelta(days=1)

    with open("all_matches.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("✔ Sparat: all_matches.json")


if __name__ == "__main__":
    date_from = "2025-04-01"
    date_to   = "2025-09-30"

    asyncio.run(fetch_range_merge(date_from, date_to))
