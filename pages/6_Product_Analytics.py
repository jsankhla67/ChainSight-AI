import streamlit as st
import plotly.express as px
from utils.database import run_query

st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
    layout="wide"
)

st.title("Product Analytics")
st.markdown("---")


# KPI CARDS


kpi = run_query("""
SELECT
    COUNT(*) AS total_products,
    ROUND(AVG(product_weight_g),2) AS avg_weight,
    ROUND(AVG(product_length_cm),2) AS avg_length,
    ROUND(AVG(product_photos_qty),2) AS avg_photos
FROM products;
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Products", f"{kpi.loc[0,'total_products']:,}")
c2.metric("Avg Weight (g)", kpi.loc[0,"avg_weight"])
c3.metric("Avg Length (cm)", kpi.loc[0,"avg_length"])
c4.metric(" Avg Photos", kpi.loc[0,"avg_photos"])

st.markdown("---")


# CATEGORY DISTRIBUTION


category = run_query("""
SELECT
    ct.product_category_name_english AS category,
    COUNT(*) AS total_products
FROM products p
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
GROUP BY category
ORDER BY total_products DESC
LIMIT 15;
""")

fig = px.bar(
    category,
    x="total_products",
    y="category",
    orientation="h",
    title="Product Category Distribution",
    color="total_products"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)


# PRODUCT WEIGHT DISTRIBUTION


weight = run_query("""
SELECT
    product_weight_g
FROM products
WHERE product_weight_g IS NOT NULL;
""")

fig2 = px.histogram(
    weight,
    x="product_weight_g",
    nbins=40,
    title=" Product Weight Distribution"
)

st.plotly_chart(fig2, use_container_width=True)


# PRODUCT DIMENSIONS


dimension = run_query("""
SELECT
    product_length_cm,
    product_width_cm,
    product_height_cm
FROM products
WHERE product_length_cm IS NOT NULL
AND product_width_cm IS NOT NULL
AND product_height_cm IS NOT NULL;
""")

fig3 = px.scatter(
    dimension,
    x="product_length_cm",
    y="product_width_cm",
    color="product_height_cm",
    title=" Product Dimensions"
)

st.plotly_chart(fig3, use_container_width=True)


# TOP PRODUCTS


top = run_query("""
SELECT
    oi.product_id,
    COUNT(*) AS quantity,
    ROUND(SUM(price),2) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY revenue DESC
LIMIT 20;
""")

st.subheader(" Top Products by Revenue")

st.dataframe(top, use_container_width=True)


# PRODUCT PHOTO ANALYSIS


photos = run_query("""
SELECT
    product_photos_qty,
    COUNT(*) AS total_products
FROM products
GROUP BY product_photos_qty
ORDER BY product_photos_qty;
""")

fig4 = px.bar(
    photos,
    x="product_photos_qty",
    y="total_products",
    title="📸 Product Photos Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

st.success("Product Analytics Loaded Successfully 🚀")