import streamlit as st
import plotly.express as px
from utils.database import run_query

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🏠 Executive Dashboard")
st.markdown("---")

# KPI CARDS


kpi_query = """
SELECT
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM orders) AS total_orders,
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM sellers) AS total_sellers,
    (SELECT ROUND(SUM(payment_value),2) FROM payments) AS total_revenue,
    (SELECT ROUND(AVG(payment_value),2) FROM payments) AS average_order_value;
"""

kpi = run_query(kpi_query)

col1, col2, col3 = st.columns(3)

col1.metric("👥 Customers", f"{kpi.loc[0,'total_customers']:,}")
col2.metric("📦 Orders", f"{kpi.loc[0,'total_orders']:,}")
col3.metric("🛍 Products", f"{kpi.loc[0,'total_products']:,}")

col4, col5, col6 = st.columns(3)

col4.metric("🏪 Sellers", f"{kpi.loc[0,'total_sellers']:,}")
col5.metric("💰 Revenue", f"${kpi.loc[0,'total_revenue']:,.2f}")
col6.metric("🧾 Avg Order Value", f"${kpi.loc[0,'average_order_value']:,.2f}")

st.markdown("---")


# MONTHLY REVENUE TREND


monthly_sales = run_query("""
SELECT
    CONCAT(
        EXTRACT(YEAR FROM o.order_purchase_timestamp),
        '-',
        LPAD(EXTRACT(MONTH FROM o.order_purchase_timestamp),2,'0')
    ) AS month,
    ROUND(SUM(p.payment_value),2) AS revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;
""")

fig = px.line(
    monthly_sales,
    x="month",
    y="revenue",
    markers=True,
    title="📈 Monthly Revenue Trend"
)

fig.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# PAYMENT METHODS


left, right = st.columns(2)

with left:

    payment = run_query("""
    SELECT
        payment_type,
        COUNT(*) AS total_orders
    FROM payments
    GROUP BY payment_type
    ORDER BY total_orders DESC;
    """)

    fig2 = px.pie(
        payment,
        names="payment_type",
        values="total_orders",
        title="💳 Payment Methods"
    )

    st.plotly_chart(fig2, use_container_width=True)

# TOP CATEGORIES


with right:

    category = run_query("""
    SELECT
        ct.product_category_name_english,
        ROUND(SUM(oi.price),2) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    JOIN category_translation ct
        ON p.product_category_name = ct.product_category_name
    GROUP BY ct.product_category_name_english
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    fig3 = px.bar(
        category,
        x="revenue",
        y="product_category_name_english",
        orientation="h",
        title="🏆 Top Categories by Revenue"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# ORDERS BY STATE


state = run_query("""
SELECT
    customer_state,
    COUNT(*) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY customer_state
ORDER BY total_orders DESC;
""")

fig4 = px.bar(
    state,
    x="customer_state",
    y="total_orders",
    title="📍 Orders by State"
)

st.plotly_chart(fig4, use_container_width=True)

# TOP PRODUCTS


products = run_query("""
SELECT
    oi.product_id,
    COUNT(*) AS total_sales,
    ROUND(SUM(price),2) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY revenue DESC
LIMIT 10;
""")

st.subheader("🏆 Top 10 Products")

st.dataframe(
    products,
    use_container_width=True
)

st.markdown("---")

st.success("Executive Dashboard Loaded Successfully 🚀")