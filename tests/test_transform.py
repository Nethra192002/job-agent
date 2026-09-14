from datetime import date

from transform import parse_date, normalize_jooble, normalize_many


SAMPLE_RAW = {
    "id": 12345,
    "title": "ML Engineer",
    "company": "Acme",
    "location": "Dublin",
    "snippet": "some description",
    "link": "https://ie.jooble.org/jdp/12345",
    "updated": "2026-09-11T00:00:00.0000000",
    "salary": "",
}


def test_parse_date_valid():
    assert parse_date("2026-09-11T00:00:00.0000000") == date(2026, 9, 11)


def test_parse_date_empty():
    assert parse_date("") is None
    assert parse_date(None) is None


def test_parse_date_malformed():
    assert parse_date("not a date") is None


def test_normalize_jooble_maps_fields():
    record = normalize_jooble(SAMPLE_RAW)
    assert record["source"] == "jooble"
    assert record["source_job_id"] == "12345"
    assert record["title"] == "ML Engineer"
    assert record["description"] == "some description"
    assert record["url"] == "https://ie.jooble.org/jdp/12345"
    assert record["posted_date"] == date(2026, 9, 11)
    assert record["salary_min"] is None


def test_normalize_jooble_stringifies_id():
    #jooble ids arrive as ints, our column is text
    record = normalize_jooble(SAMPLE_RAW)
    assert isinstance(record["source_job_id"], str)


def test_normalize_many_skips_missing_id():
    raw_jobs = [SAMPLE_RAW, {"title": "no id job", "snippet": "x"}]
    records = normalize_many(raw_jobs, normalize_jooble)
    assert len(records) == 1
    assert records[0]["source_job_id"] == "12345"