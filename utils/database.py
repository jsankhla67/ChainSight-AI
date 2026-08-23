import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured. "
        "Add DATABASE_URL to Streamlit Cloud Secrets."
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def get_connection():
    return engine.connect()


def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def run_query(query):
    """Execute SQL and return results as a pandas DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
