# WORKING OF AI ASSISTANT

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ai.prompts import SQL_SYSTEM_PROMPT, ANSWER_SYSTEM_PROMPT
from ai.tools import get_database_schema, execute_sql


load_dotenv()


# NVIDIA API KEY

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY is not set in .env")


# NVIDIA MODEL

# Yaha NVIDIA ka OpenAI compatible API use kr rhe hai
# Isse hum LangChain ke through NVIDIA model ko call kr sakte hai

chat_model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=NVIDIA_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1",
    temperature=0.1, # controls randomness of AI responses
    max_tokens=1024, # maximum number of tokens in the AI response
)


# SQL VALIDATION - safety check.

def validate_sql(sql: str) -> bool:

    if not sql:
        raise ValueError("AI generated an empty SQL query.") # if AI generated empty SQL query

    sql_clean = sql.strip().lower() # Extra spaces/markdown remove

    # AI kabhi kabhi SQL ko markdown code block ke andar return kr deta hai
    # Isliye yaha unwanted markdown remove kr rhe hai

    sql_clean = sql_clean.replace("```sql", "")
    sql_clean = sql_clean.replace("```mysql", "")
    sql_clean = sql_clean.replace("```", "")
    sql_clean = sql_clean.strip() # removes white space from end and begining 

    # Query SELECT ya WITH se start honi chahiye
    # Hum database me data change krne wali query allow nahi kr rhe

    if not (
        sql_clean.startswith("select")
        or sql_clean.startswith("with")
    ):
        raise ValueError(
            "Only read-only SELECT queries are allowed."
        )

    # Dangerous SQL keywords ko yaha block kr rhe hai

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


# YAHA PR APN SQL FUNCTION BNA RHE HAI JO KI NATURAL LANGUAGE QUESTION
# KO MYSQL SELECT QUERY ME CONVERT KREGA

def generate_sql(question: str):

    # Sabse pehle database ka schema le rhe hai
    # AI ko pata hona chahiye ki database me kaunse tables aur columns hai

    schema = get_database_schema()

    # SQL ke liye prompt create kr rhe hai

    prompt = ChatPromptTemplate.from_template(
        SQL_SYSTEM_PROMPT
    )

    # Prompt ko NVIDIA model ke saath connect kr rhe hai

    chain = prompt | chat_model 

    # User ka question aur database schema AI ko bhej rhe hai

    response = chain.invoke(
        {
            "schema": schema,
            "question": question,
        }
    )

    # AI ke response ko string me convert kr rhe hai

    sql = response.content.strip()

    # AI agar SQL ko markdown code block me return kare
    # to usko remove kr denge

    sql = sql.replace("```sql", "")
    sql = sql.replace("```mysql", "")
    sql = sql.replace("```", "")

    sql = sql.strip()

    # SQL execute karne se pehle security validation

    validate_sql(sql)

    return sql


# DATABASE RESULTS KO HUMAN READABLE BUSINESS ANSWER ME CONVERT KRNE KE LIYE

def generate_business_answer( question: str, sql: str, results ) -> str:

    # Business answer ke liye alag prompt use kr rhe hai

    prompt = ChatPromptTemplate.from_template(
        ANSWER_SYSTEM_PROMPT
    )

    # Prompt ko NVIDIA model ke saath connect kr rhe hai

    chain = prompt | chat_model

    # User question, generated SQL aur database results
    # AI ko bhej rhe hai taaki wo business explanation de sake

    response = chain.invoke(
        {
            "question": question,
            "sql": sql,
            "results": results,
        }
    )

    return response.content.strip()


# COMPLETE BUSINESS ANALYST PIPELINE

def ask_business_question(question: str):

    # Step 1:
    # Natural language question ko SQL query me convert krna

    sql = generate_sql(question)

    # Step 2:
    # Generated SQL ko dobara validate krna

    validate_sql(sql)

    # Step 3:
    # Valid SQL ko database me execute krna

    results = execute_sql(sql)

    # Step 4:
    # Database ke results ko human readable business answer me convert krna

    answer = generate_business_answer(
        question,
        sql,
        results
    )

    # Saari information ek dictionary ke form me return kr rhe hai

    return {
        "question": question,
        "sql": sql,
        "results": results,
        "answer": answer,
    }