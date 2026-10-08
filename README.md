# 🔗 ChainSight AI

### AI-Powered E-Commerce Supply Chain Intelligence

ChainSight AI is an AI-powered Business Intelligence platform that combines interactive Streamlit dashboards with a natural-language AI Business Analyst.

Users can ask business questions in plain English, and the system automatically generates SQL, queries MySQL, analyzes the results, and provides business insights with visualizations.

## Features

- Executive, Sales, Customer, Product, Supply Chain & Review dashboards
- AI Business Analyst for natural-language data queries
- LangChain + Hugging Face LLM integration
- MySQL database with 17 analytical tables
- Read-only SQL validation for safe AI database access
- Automatic Plotly visualizations
- CSV export for AI-generated results

🛠️ Tech Stack

Python · Streamlit · MySQL · SQLAlchemy · PyMySQL · Pandas · NumPy · Plotly · LangChain · Hugging Face

Dataset

Built using the Brazilian E-Commerce Public Dataset by Olist, containing approximately 99K+ e-commerce records across customers, orders, products, sellers, payments, reviews, and delivery data.

⚙️ Setup
git clone https://github.com/jsankhla67/E-Commerce-Supply-Chain-Intelligence.git
cd E-Commerce-Supply-Chain-Intelligence

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

Create a .env file:

DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/ecommerce_supply_chain
HF_TOKEN=your_huggingface_api_token

Run:

streamlit run app.py

💡 Example

Ask:

What are the top 5 product categories by sales?
or whatever u like to ask 

ChainSight AI generates the SQL, retrieves the data from MySQL, explains the results, and automatically creates a visualization.


Author

Jatin Sankhla

