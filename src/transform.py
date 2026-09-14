from datetime import datetime


def parse_date(raw):
    #jooble sends an iso timestamp string, we want just the date
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw).date()
    except (ValueError, TypeError):
        return None


def normalize_jooble(raw_job):
    #map one raw jooble job dict into our common record shape
    return {
        "source": "jooble",
        "source_job_id": str(raw_job.get("id", "")),
        "title": raw_job.get("title"),
        "company": raw_job.get("company"),
        "location": raw_job.get("location"),
        "remote": False,
        "description": raw_job.get("snippet"),
        "url": raw_job.get("link"),
        "posted_date": parse_date(raw_job.get("updated")),
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
    }


def normalize_many(raw_jobs, normalizer):
    #run a list of raw jobs through a chosen normalizer, skipping any that lack an id
    records = []
    for raw in raw_jobs:
        record = normalizer(raw)
        if record["source_job_id"]:
            records.append(record)
    return records


if __name__ == "__main__":
    from sources.jooble import fetch_jobs

    raw = fetch_jobs(keywords="machine learning", location="Dublin")
    records = normalize_many(raw, normalize_jooble)

    print(f"normalized {len(records)} of {len(raw)} raw jobs")
    if records:
        sample = records[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")