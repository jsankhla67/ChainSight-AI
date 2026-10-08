import streamlit as st
import plotly.express as px
from utils.database import run_query

st.set_page_config(
    page_title="Review Analytics",
    page_icon="⭐",
    layout="wide"
)

st.title("Review Analytics")
st.markdown("---")


# KPI CARDS


kpi = run_query("""
SELECT
    ROUND(AVG(review_score),2) AS avg_rating,
    COUNT(*) AS total_reviews,
    MIN(review_score) AS lowest_rating,
    MAX(review_score) AS highest_rating
FROM reviews;
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Rating", kpi.loc[0, "avg_rating"])
c2.metric("Total Reviews", f"{kpi.loc[0, 'total_reviews']:,}")
c3.metric(" Lowest Rating", kpi.loc[0, "lowest_rating"])
c4.metric("Highest Rating", kpi.loc[0, "highest_rating"])

st.markdown("---")


# REVIEW DISTRIBUTION


review_dist = run_query("""
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM reviews
GROUP BY review_score
ORDER BY review_score;
""")

fig = px.bar(
    review_dist,
    x="review_score",
    y="total_reviews",
    text="total_reviews",
    title="⭐ Review Score Distribution"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)


# REVIEWS OVER TIME


review_time = run_query("""
SELECT
    CONCAT(
        EXTRACT(YEAR FROM review_creation_date),
        '-',
        LPAD(EXTRACT(MONTH FROM review_creation_date),2,'0')
    ) AS month,
    COUNT(*) AS reviews
FROM reviews
GROUP BY month
ORDER BY month;
""")

fig2 = px.line(
    review_time,
    x="month",
    y="reviews",
    markers=True,
    title="📈 Reviews Over Time"
)

fig2.update_layout(template="plotly_white")

st.plotly_chart(fig2, use_container_width=True)


# CATEGORY RATINGS

category = run_query("""
SELECT
    ct.product_category_name_english AS category,
    ROUND(AVG(r.review_score),2) AS rating,
    COUNT(*) AS reviews

FROM reviews r

JOIN orders o
    ON r.order_id = o.order_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name

GROUP BY category

HAVING COUNT(*) > 50

ORDER BY rating DESC

LIMIT 15;
""")

fig3 = px.bar(
    category,
    x="rating",
    y="category",
    orientation="h",
    color="rating",
    title="🏆 Highest Rated Categories"
)

st.plotly_chart(fig3, use_container_width=True)


# REVIEW SCORE SHARE


pie = run_query("""
SELECT
    review_score,
    COUNT(*) AS total
FROM reviews
GROUP BY review_score;
""")

fig4 = px.pie(
    pie,
    names="review_score",
    values="total",
    title="⭐ Review Score Share"
)

st.plotly_chart(fig4, use_container_width=True)


# RECENT REVIEWS


recent = run_query("""
SELECT
    review_id,
    review_score,
    review_creation_date,
    LEFT(review_comment_message,100) AS comment

FROM reviews

WHERE review_comment_message IS NOT NULL

ORDER BY review_creation_date DESC

LIMIT 20;
""")

st.subheader("📝 Recent Customer Reviews")

st.dataframe(recent, use_container_width=True)

st.success("Review Analytics Loaded Successfully 🚀")