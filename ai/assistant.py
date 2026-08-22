import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate

from ai.prompts import SQL_SYSTEM_PROMPT, ANSWER_SYSTEM_PROMPT
from ai.tools import get_database_schema, execute_sql


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is not set in .env")


# =========================================================
# HUGGING FACE MODEL
# =========================================================

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-4B-Instruct-2507",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.1,
    max_new_tokens=512,
)

chat_model = ChatHuggingFace(llm=llm)


# =========================================================
# SQL VALIDATION
# =========================================================

def validate_sql(sql: str) -> bool:
    """
    Validate that the AI generated query is read-only.

    Only SELECT queries are allowed.
    """

    if not sql:
        raise ValueError("AI generated an empty SQL query.")

    sql_clean = sql.strip().lower()

    # Remove accidental markdown
    sql_clean = sql_clean.replace("```sql", "")
    sql_clean = sql_clean.replace("```mysql", "")
    sql_clean = sql_clean.replace("```", "")
    sql_clean = sql_clean.strip()

    # Must start with SELECT or WITH
    if not (
        sql_clean.startswith("select")
        or sql_clean.startswith("with")
    ):
        raise ValueError(
            "Only read-only SELECT queries are allowed."
        )

    # Dangerous SQL operations
    forbidden_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "replace ",
        "grant ",
        "revoke ",
    ]

    for keyword in forbidden_keywords:

        if keyword in sql_clean:

            raise ValueError(
                f"Unsafe SQL detected: {keyword.strip()}"
            )

    return True


# =========================================================
# GENERATE SQL
# =========================================================

def generate_sql(question: str) -> str:
    """
    Convert a natural-language business question
    into a MySQL SELECT query.
    """

    schema = get_database_schema()

    prompt = ChatPromptTemplate.from_template(
        SQL_SYSTEM_PROMPT
    )

    chain = prompt | chat_model

    response = chain.invoke(
        {
            "schema": schema,
            "question": question,
        }
    )

    sql = response.content.strip()

    # Remove accidental markdown code fences
    sql = sql.replace("```sql", "")
    sql = sql.replace("```mysql", "")
    sql = sql.replace("```", "")

    sql = sql.strip()

    # Validate immediately
    validate_sql(sql)

    return sql


# =========================================================
# GENERATE BUSINESS ANSWER
# =========================================================

def generate_business_answer(
    question: str,
    sql: str,
    results
) -> str:
    """
    Convert database results into a
    human-readable business explanation.
    """

    prompt = ChatPromptTemplate.from_template(
        ANSWER_SYSTEM_PROMPT
    )

    chain = prompt | chat_model

    response = chain.invoke(
        {
            "question": question,
            "sql": sql,
            "results": results,
        }
    )

    return response.content.strip()


# =========================================================
# COMPLETE BUSINESS ANALYST PIPELINE
# =========================================================

def ask_business_question(question: str):
    """
    Complete AI Business Analyst pipeline:

    User Question
        ↓
    Hugging Face
        ↓
    SQL Generation
        ↓
    SQL Safety Validation
        ↓
    MySQL
        ↓
    Results
        ↓
    Business Explanation
    """

    # -----------------------------------------------------
    # 1. Generate SQL
    # -----------------------------------------------------

    sql = generate_sql(question)

    # -----------------------------------------------------
    # 2. Validate SQL again before database execution
    # -----------------------------------------------------

    validate_sql(sql)

    # -----------------------------------------------------
    # 3. Execute SQL
    # -----------------------------------------------------

    results = execute_sql(sql)

    # -----------------------------------------------------
    # 4. Generate business explanation
    # -----------------------------------------------------

    answer = generate_business_answer(
        question,
        sql,
        results
    )

    return {
        "question": question,
        "sql": sql,
        "results": results,
        "answer": answer,
    }