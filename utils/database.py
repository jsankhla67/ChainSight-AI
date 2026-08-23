import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# Load .env for local development
load_dotenv()


# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------
# Streamlit Cloud:
#     st.secrets["DATABASE_URL"]
#
# Local development:
#     .env -> DATABASE_URL
# ---------------------------------------------------------

DATABASE_URL = None

# First try Streamlit Secrets
try:
    DATABASE_URL = st.secrets.get("DATABASE_URL")
except Exception:
    DATABASE_URL = None

# If Streamlit Secrets doesn't contain it,
# try the local environment variable
if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")


# Stop with a clear message if neither exists
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured. "
        "Add DATABASE_URL to Streamlit Cloud Secrets "
        "or to your local .env file."
    )


# ---------------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ---------------------------------------------------------
# CONNECTION
# ---------------------------------------------------------

def get_connection():
    return engine.connect()


# ---------------------------------------------------------
# TEST CONNECTION
# ---------------------------------------------------------

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return True

    except Exception:
        return False


# ---------------------------------------------------------
# RUN SQL QUERY
# ---------------------------------------------------------

def run_query(query):
    """
    Execute SQL and return results as a pandas DataFrame.
    """

    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
