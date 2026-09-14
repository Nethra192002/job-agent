import os
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def clean_html(text):
    #strip html tags and entities jooble leaves in the snippet
    if not text:
        return ""
    return BeautifulSoup(text, "html.parser").get_text().strip()


@st.cache_resource
def get_engine():
    #tell sqlalchemy to use psycopg v3, the driver we actually have installed
    engine_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
    return create_engine(engine_url, pool_pre_ping=True)

@st.cache_data(ttl=300)
def load_jobs():
    #read all jobs into a dataframe, cached for 5 minutes
    engine = get_engine()
    df = pd.read_sql_query(
        "select title, company, location, description, url, posted_date, source "
        "from jobs order by posted_date desc nulls last",
        engine,
    )
    df["description"] = df["description"].apply(clean_html)
    return df


st.set_page_config(page_title="Job Agent", layout="wide")
st.title("Job Agent")

df = load_jobs()
st.caption(f"{len(df)} jobs in the database")

#filter controls in the sidebar
st.sidebar.header("Filters")

keyword = st.sidebar.text_input("Keyword (title or description)")

locations = sorted(df["location"].dropna().unique().tolist())
location = st.sidebar.selectbox("Location", ["All"] + locations)

#apply the filters to a working copy
filtered = df.copy()

if keyword:
    mask = (
        filtered["title"].str.contains(keyword, case=False, na=False)
        | filtered["description"].str.contains(keyword, case=False, na=False)
    )
    filtered = filtered[mask]

if location != "All":
    filtered = filtered[filtered["location"] == location]

st.write(f"showing {len(filtered)} jobs")

#render as a table with clickable links
st.dataframe(
    filtered,
    column_config={
        "url": st.column_config.LinkColumn("Apply", display_text="open"),
        "posted_date": "Posted",
        "title": "Title",
        "company": "Company",
        "location": "Location",
        "description": "Description",
        "source": "Source",
    },
    hide_index=True,
    use_container_width=True,
)