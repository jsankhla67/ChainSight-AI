import streamlit as st
import plotly.express as px
from utils.database import run_query

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Sales Analytics")
st.markdown("---")


# KPI CARDS


kpi = run_query("""
SELECT
    ROUND(SUM(payment_value),2) AS revenue,
    ROUND(AVG(payment_value),2) AS avg_order,
    MAX(payment_value) AS highest_order,
    COUNT(DISTINCT order_id) AS total_orders
FROM payments;
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Revenue", f"${kpi.loc[0,'revenue']:,.2f}")
c2.metric("📦 Orders", f"{kpi.loc[0,'total_orders']:,}")
c3.metric("🧾 Avg Order", f"${kpi.loc[0,'avg_order']:,.2f}")
c4.metric("🏆 Highest Order", f"${kpi.loc[0,'highest_order']:,.2f}")

st.markdown("---")


# MONTHLY SALES


monthly = run_query("""
SELECT
    CONCAT(
        EXTRACT(YEAR FROM o.order_purchase_timestamp),
        '-',
        LPAD(EXTRACT(MONTH FROM o.order_purchase_timestamp),2,'0')
    ) AS month,
    ROUND(SUM(payment_value),2) AS revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;
""")

fig = px.line(
    monthly,
    x="month",
    y="revenue",
    markers=True,
    title="📈 Monthly Revenue"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)


# CATEGORY REVENUE


left, right = st.columns(2)

with left:

    category = run_query("""
    SELECT
        ct.product_category_name_english AS category,
        ROUND(SUM(price),2) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    LEFT JOIN category_translation ct
        ON p.product_category_name = ct.product_category_name
    GROUP BY category
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    fig2 = px.bar(
        category,
        x="revenue",
        y="category",
        orientation="h",
        title="🏆 Top Categories"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:

    seller = run_query("""
    SELECT
        seller_id,
        ROUND(SUM(price),2) AS revenue
    FROM order_items
    GROUP BY seller_id
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    fig3 = px.bar(
        seller,
        x="revenue",
        y="seller_id",
        orientation="h",
        title="🏪 Top Sellers"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# PAYMENT TYPES


payment = run_query("""
SELECT
    payment_type,
    COUNT(*) AS orders
FROM payments
GROUP BY payment_type;
""")

fig4 = px.pie(
    payment,
    names="payment_type",
    values="orders",
    title="💳 Payment Methods"
)

st.plotly_chart(fig4, use_container_width=True)


# TOP PRODUCTS


products = run_query("""
SELECT
    oi.product_id,
    COUNT(*) AS quantity,
    ROUND(SUM(price),2) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY revenue DESC
LIMIT 15;
""")

st.subheader("🏆 Top Products")

st.dataframe(products, use_container_width=True)

st.success("Sales Analytics Loaded Successfully 🚀")