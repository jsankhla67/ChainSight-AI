import streamlit as st
import plotly.express as px
from utils.database import run_query

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Supply Chain Analytics")
st.markdown("---")


# KPI CARDS


kpi = run_query("""
SELECT
    ROUND(
        AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)), 2
    ) AS avg_delivery,

    ROUND(
        AVG(DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp)), 2
    ) AS estimated_delivery,

    COUNT(*) AS delivered_orders

FROM orders

WHERE order_delivered_customer_date IS NOT NULL;
""")

late = run_query("""
SELECT
    COUNT(*) AS late_orders
FROM orders
WHERE order_delivered_customer_date > order_estimated_delivery_date;
""")

freight = run_query("""
SELECT
    ROUND(AVG(freight_value),2) AS avg_freight,
    ROUND(SUM(freight_value),2) AS total_freight
FROM order_items;
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Delivered Orders", f"{kpi.loc[0,'delivered_orders']:,}")
c2.metric("🚚 Avg Delivery", f"{kpi.loc[0,'avg_delivery']} Days")
c3.metric("⏱ Estimated Delivery", f"{kpi.loc[0,'estimated_delivery']} Days")
c4.metric("⚠ Late Deliveries", f"{late.loc[0,'late_orders']:,}")

st.markdown("---")


# DELIVERY TREND


delivery = run_query("""
SELECT

    CONCAT(
        EXTRACT(YEAR FROM order_purchase_timestamp),
        '-',
        LPAD(EXTRACT(MONTH FROM order_purchase_timestamp),2,'0')
    ) AS month,

    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),2
    ) AS delivery_days

FROM orders

WHERE order_delivered_customer_date IS NOT NULL

GROUP BY month

ORDER BY month;
""")

fig = px.line(
    delivery,
    x="month",
    y="delivery_days",
    markers=True,
    title="📈 Average Delivery Time"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)


# TWO CHARTS


left, right = st.columns(2)

with left:

    freight_state = run_query("""
    SELECT
        seller_state,
        ROUND(AVG(freight_value),2) AS freight
    FROM sellers s
    JOIN order_items oi
        ON s.seller_id = oi.seller_id
    GROUP BY seller_state
    ORDER BY freight DESC;
    """)

    fig2 = px.bar(
        freight_state,
        x="seller_state",
        y="freight",
        title="💲 Average Freight by Seller State"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:

    seller = run_query("""
    SELECT
        seller_id,
        COUNT(*) AS orders,
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


# DELIVERY STATUS


status = run_query("""
SELECT

CASE
    WHEN order_delivered_customer_date <= order_estimated_delivery_date
        THEN 'On Time'
    ELSE 'Late'
END AS status,

COUNT(*) AS total

FROM orders

WHERE order_delivered_customer_date IS NOT NULL

GROUP BY status;
""")

fig4 = px.pie(
    status,
    names="status",
    values="total",
    title="📦 Delivery Status"
)

st.plotly_chart(fig4, use_container_width=True)


# TOP SHIPPING COST


shipping = run_query("""
SELECT
    order_id,
    freight_value
FROM order_items
ORDER BY freight_value DESC
LIMIT 20;
""")

st.subheader("🚛 Highest Shipping Cost Orders")

st.dataframe(shipping, use_container_width=True)

st.success("Supply Chain Dashboard Loaded Successfully 🚀")