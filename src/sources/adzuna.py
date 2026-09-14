import os
import requests
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def fetch_jobs(what, where="", country="ie", results_per_page=50, max_days_old=7):
    #build the request url for the given country
    url = f"{BASE_URL}/{country}/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": what,
        "where": where,
        "max_days_old": max_days_old,
        "content-type": "application/json",
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        print(f"status: {response.status_code}")
        print(f"body: {response.text}")
        response.raise_for_status()

    data = response.json()
    return data.get("results", [])


if __name__ == "__main__":
    jobs = fetch_jobs(what="machine learning", where="Dublin")
    print(f"fetched {len(jobs)} jobs")
    if jobs:
        first = jobs[0]
        print("sample job keys:", list(first.keys()))
        print("title:", first.get("title"))
        print("company:", first.get("company"))