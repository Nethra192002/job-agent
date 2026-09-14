import os
import requests
from dotenv import load_dotenv

load_dotenv()

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

BASE_URL = "https://ie.jooble.org/api"


def fetch_jobs(keywords, location="Ireland", page=1):
    #jooble puts the api key in the url path, not in the params
    url = f"{BASE_URL}/{JOOBLE_API_KEY}"

    payload = {
        "keywords": keywords,
        "location": location,
        "page": str(page),
    }

    response = requests.post(url, json=payload, timeout=30)

    if response.status_code != 200:
        print(f"status: {response.status_code}")
        print(f"body: {response.text}")
        response.raise_for_status()

    data = response.json()
    return data.get("jobs", [])


if __name__ == "__main__":
    jobs = fetch_jobs(keywords="machine learning", location="Dublin")
    print(f"fetched {len(jobs)} jobs")
    if jobs:
        first = jobs[0]
        print("sample job keys:", list(first.keys()))
        print("title:", first.get("title"))
        print("company:", first.get("company")) 