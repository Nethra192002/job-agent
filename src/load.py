import os
import psycopg # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

UPSERT_SQL = """
insert into jobs (
    source, source_job_id, title, company, location,
    remote, description, url, posted_date,
    salary_min, salary_max, salary_currency
)
values (
    %(source)s, %(source_job_id)s, %(title)s, %(company)s, %(location)s,
    %(remote)s, %(description)s, %(url)s, %(posted_date)s,
    %(salary_min)s, %(salary_max)s, %(salary_currency)s
)
on conflict (source, source_job_id) do update set
    title = excluded.title,
    company = excluded.company,
    location = excluded.location,
    description = excluded.description,
    url = excluded.url,
    posted_date = excluded.posted_date
"""


def save_jobs(records):
    #write normalized records to postgres, skipping duplicates via upsert
    if not records:
        return 0

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            for record in records:
                cur.execute(UPSERT_SQL, record)
        conn.commit()

    return len(records)


if __name__ == "__main__":
    from sources.jooble import fetch_jobs
    from transform import normalize_jooble, normalize_many

    raw = fetch_jobs(keywords="machine learning", location="Dublin")
    records = normalize_many(raw, normalize_jooble)
    count = save_jobs(records)
    print(f"saved {count} jobs to the database")