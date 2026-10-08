import streamlit as st
import plotly.express as px
from utils.database import run_query

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Analytics")
st.markdown("---")


# KPI CARDS


kpi = run_query("""
SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;
""")

repeat = run_query("""
SELECT COUNT(*) AS repeat_customers
FROM (
    SELECT c.customer_unique_id
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
    HAVING COUNT(o.order_id) > 1
) t;
""")

avg_orders = run_query("""
SELECT
    ROUND(AVG(order_count),2) AS avg_orders
FROM(
    SELECT
        customer_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
)x;
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Customers", f"{kpi.loc[0,'total_customers']:,}")
c2.metric("Unique Customers", f"{kpi.loc[0,'unique_customers']:,}")
c3.metric("Repeat Customers", f"{repeat.loc[0,'repeat_customers']:,}")
c4.metric("Avg Orders / Customer", avg_orders.loc[0,"avg_orders"])

st.markdown("---")


# CUSTOMER GROWTH


growth = run_query("""
SELECT
    CONCAT(
        EXTRACT(YEAR FROM order_purchase_timestamp),
        '-',
        LPAD(EXTRACT(MONTH FROM order_purchase_timestamp),2,'0')
    ) AS month,
    COUNT(DISTINCT customer_id) AS customers
FROM orders
GROUP BY month
ORDER BY month;
""")

fig = px.line(
    growth,
    x="month",
    y="customers",
    markers=True,
    title="📈 Customer Growth"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)


# TWO CHARTS


left, right = st.columns(2)

with left:

    state = run_query("""
    SELECT
        customer_state,
        COUNT(*) AS customers
    FROM customers
    GROUP BY customer_state
    ORDER BY customers DESC;
    """)

    fig2 = px.bar(
        state,
        x="customer_state",
        y="customers",
        title="🏙 Customers by State"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:

    top = run_query("""
    SELECT
        c.customer_unique_id,
        ROUND(SUM(p.payment_value),2) AS revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY c.customer_unique_id
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    fig3 = px.bar(
        top,
        x="revenue",
        y="customer_unique_id",
        orientation="h",
        title="💰 Top 10 Customers"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# CUSTOMER SEGMENTATION


segment = run_query("""
SELECT
CASE
    WHEN total_spent >= 1000 THEN 'VIP'
    WHEN total_spent >= 500 THEN 'Gold'
    WHEN total_spent >= 200 THEN 'Silver'
    ELSE 'Regular'
END AS customer_segment,

COUNT(*) AS customers

FROM (

SELECT
    c.customer_unique_id,
    SUM(payment_value) AS total_spent

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN payments p
    ON o.order_id = p.order_id

GROUP BY c.customer_unique_id

)x

GROUP BY customer_segment;
""")

fig4 = px.pie(
    segment,
    names="customer_segment",
    values="customers",
    title="👤 Customer Segments"
)

st.plotly_chart(fig4, use_container_width=True)


# CUSTOMER TABLE


table = run_query("""
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(payment_value),2) AS total_spent,
    ROUND(AVG(payment_value),2) AS average_order

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN payments p
    ON o.order_id = p.order_id

GROUP BY c.customer_unique_id

ORDER BY total_spent DESC

LIMIT 20;
""")

st.subheader("🏆 Top Customers")

st.dataframe(table, use_container_width=True)

st.success("Customer Analytics Loaded Successfully 🚀")