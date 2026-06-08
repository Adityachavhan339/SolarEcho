import os
import aiohttp
import asyncio 
from datetime import datetime, timedelta


BASE_URL = "https://api.nasa.gov/DONKI/CME"
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

async def fetch_recent_cmes(session: aiohttp.ClientSession, api_key: str, days: int = 7):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    params = { 
        "startDate": start.strftime("%Y-%m-%d"),
        "endDate": end.strftime("%Y-%m-%d"),
        "api_key": api_key
    }
    async with session.get(BASE_URL, params=params,timeout=aiohttp.ClientTimeout(total=30)) as resp:
        if resp.status == 200:
            return await resp.json()
        text = await resp.text()
        raise RuntimeError(f"NASA API returned {resp.status}: {text}")

def extract_latest_features(cme_list: list):
    if not cme_list:
        return None

    for cme in reversed(cme_list):
        analyses = cme.get("cmeAnalyses", [])
        if not analyses:
            continue

        for a in analyses:
            speed = a.get("speed")
            if speed is None:
                continue

            return {
                "speed": float(speed),
                "halfAngle": float(a.get("halfAngle", 30.0) or 30.0),
                "latitude": float(a.get("latitude", 0.0) or 0.0),
                "longitude": float(a.get("longitude", 0.0) or 0.0),
                "activity_id": cme.get("activityID", "unknown"),
            }

    return None

async def cme_poller(queue: asyncio.Queue, api_key: str, interval: int = 60):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                data = await fetch_recent_cmes(session, api_key)
                features = extract_latest_features(data)
                if features:
                    await queue.put(features)
                    print(f"[NASA] CME {features['activity_id']} | "
                          f"speed={features['speed']:.0f} km/s | "
                          f"halfAngle={features['halfAngle']:.1f} | "
                          f"lat={features['latitude']:.1f} | "
                          f"lon={features['longitude']:.1f}")
                else:
                    print("[NASA] No recent CMEs with analysis data. Will retry...")
            except Exception as e:
                print(f"Error fetching CME data: {e}")
            await asyncio.sleep(interval)

