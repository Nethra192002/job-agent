create table if not exists jobs (
    id bigint generated always as identity primary key,
    source text not null,
    source_job_id text not null,
    title text not null,
    company text,
    location text,
    remote boolean default false,
    description text,
    url text,
    posted_date date,
    salary_min numeric,
    salary_max numeric,
    salary_currency text,
    ingested_at timestamptz default now(),
    unique (source, source_job_id)
);