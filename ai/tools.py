from sqlalchemy import text
from utils.database import engine


def get_database_schema():
    """Return the database tables and columns."""

    query = text("""
        SELECT
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'ecommerce_supply_chain'
        ORDER BY TABLE_NAME, ORDINAL_POSITION
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    schema = {}

    for table, column, data_type in rows:
        schema.setdefault(table, []).append(
            f"{column} ({data_type})"
        )

    return schema


def execute_sql(query: str):
    """Execute a read-only SQL query."""

    query_clean = query.strip().lower()

    forbidden = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "replace ",
    ]

    if any(word in query_clean for word in forbidden):
        raise ValueError("Only read-only SQL queries are allowed.")

    if not query_clean.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()