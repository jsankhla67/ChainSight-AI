import streamlit as st
import pandas as pd
import plotly.express as px

from ai.assistant import ask_business_question


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Business Analyst")

st.markdown(
    """
    Ask questions about your e-commerce business in plain English.

    The AI will:
    **understand your question → generate SQL → query MySQL → analyze the results**
    """
)

st.divider()


# =========================================================
# QUESTION INPUT
# =========================================================

question = st.text_input(
    "💬 Ask a business question",
    placeholder="Example: What are the top 5 product categories by sales?"
)


# =========================================================
# EXAMPLE QUESTIONS
# =========================================================

st.markdown("### 💡 Example Questions")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "📊 What are the top 5 product categories by sales?"
    )

with col2:
    st.info(
        "💰 What is the total revenue?"
    )

with col3:
    st.info(
        "📦 How many orders do we have?"
    )


# =========================================================
# RUN AI ANALYSIS
# =========================================================

if question:

    with st.spinner("🤖 Analyzing your business question..."):

        try:

            result = ask_business_question(question)

            sql = result["sql"]
            raw_results = result["results"]
            answer = result["answer"]

            # -------------------------------------------------
            # CONVERT RESULTS TO DATAFRAME
            # -------------------------------------------------

            if raw_results:

                columns = [
                    f"column_{i + 1}"
                    for i in range(len(raw_results[0]))
                ]

                df = pd.DataFrame(
                    raw_results,
                    columns=columns
                )

            else:

                df = pd.DataFrame()


            # =================================================
            # BUSINESS ANSWER
            # =================================================

            st.subheader("💡 Business Insight")

            st.markdown(answer)


            # =================================================
            # RESULTS
            # =================================================

            if not df.empty:

                st.divider()

                st.subheader("📊 Data")


                # -------------------------------------------------
                # CLEAN DATABASE VALUES
                # -------------------------------------------------

                for column in df.columns:

                    if df[column].dtype == "object":

                        df[column] = (
                            df[column]
                            .astype(str)
                            .str.replace("\r", "", regex=False)
                            .str.strip()
                        )


                # =================================================
                # KPI DETECTION
                # =================================================

                if df.shape == (1, 1):

                    value = df.iloc[0, 0]

                    st.metric(
                        label=df.columns[0].replace("_", " ").title(),
                        value=f"{value:,}"
                        if isinstance(value, (int, float))
                        else str(value)
                    )


                # =================================================
                # MULTI-COLUMN DATA
                # =================================================

                else:

                    # ---------------------------------------------
                    # DATA TABLE
                    # ---------------------------------------------

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )


                    # =================================================
                    # AUTOMATIC CHART
                    # =================================================

                    if len(df.columns) >= 2:

                        x_column = df.columns[0]
                        y_column = df.columns[1]

                        # Try to convert second column to numeric
                        numeric_values = pd.to_numeric(
                            df[y_column],
                            errors="coerce"
                        )

                        if numeric_values.notna().all():

                            chart_df = df.copy()

                            chart_df[y_column] = numeric_values

                            st.subheader("📈 Visualization")

                            # -----------------------------------------
                            # LINE CHART FOR TIME-SERIES DATA
                            # -----------------------------------------

                            if (
                                "month" in x_column.lower()
                                or "date" in x_column.lower()
                                or "year" in x_column.lower()
                            ):

                                fig = px.line(
                                    chart_df,
                                    x=x_column,
                                    y=y_column,
                                    markers=True,
                                    title=f"{y_column.replace('_', ' ').title()} by {x_column.replace('_', ' ').title()}"
                                )

                            # -----------------------------------------
                            # BAR CHART FOR RANKINGS/CATEGORIES
                            # -----------------------------------------

                            else:

                                fig = px.bar(
                                    chart_df,
                                    x=x_column,
                                    y=y_column,
                                    title=f"{y_column.replace('_', ' ').title()} by {x_column.replace('_', ' ').title()}"
                                )

                            fig.update_layout(
                                xaxis_title=x_column.replace(
                                    "_", " "
                                ).title(),

                                yaxis_title=y_column.replace(
                                    "_", " "
                                ).title()
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )


                # =================================================
                # DOWNLOAD CSV
                # =================================================

                st.divider()

                csv = df.to_csv(index=False)

                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="ai_business_analysis.csv",
                    mime="text/csv"
                )


            # =================================================
            # SQL DETAILS
            # =================================================

            with st.expander("🔍 View Generated SQL"):

                st.code(
                    sql,
                    language="sql"
                )


        except Exception as e:

            st.error(
                f"❌ Unable to analyze the question:\n\n{e}"
            )