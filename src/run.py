from sources.jooble import fetch_jobs
from transform import normalize_jooble, normalize_many
from load import save_jobs

SEARCH_TERMS = [
    "machine learning",
    "artificial intelligence",
    "data scientist",
    "ml engineer",
    "ai engineer",
    "deep learning",
]

LOCATION = "Ireland"


def run():
    #pull every search term, normalize, and load into one deduplicated batch
    all_records = []

    for term in SEARCH_TERMS:
        raw = fetch_jobs(keywords=term, location=LOCATION)
        records = normalize_many(raw, normalize_jooble)
        print(f"  '{term}': {len(raw)} raw, {len(records)} normalized")
        all_records.extend(records)

    print(f"total collected: {len(all_records)} records across {len(SEARCH_TERMS)} terms")

    saved = save_jobs(all_records)
    print(f"upserted {saved} records into the database")


if __name__ == "__main__":
    run()