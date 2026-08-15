import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import (
    load_sheet,
    clean_column_names
)


def render_promotions():

    # ====================================
    # LOAD SHEET
    # ====================================

    sheet = load_sheet(
        "10. Promotion State"
    )

    title = str(
        sheet.iloc[0, 0]
    ).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:10].copy()

    df.columns = headers

    df = clean_column_names(df)

    st.header(
        "👨‍✈️ Promotion Timelines & Vacancy State"
    )

    st.caption(title)

    # ====================================
    # NUMERIC CLEANING
    # ====================================

    numeric_cols = [
        "Held Strength",
        "Course Qualified",
        "Cadre Qualified",
        "Eligible for Next Rank",
        "Vacancies in Next Rank"
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # ====================================
    # DERIVED METRICS
    # ====================================

    df["Course Qualification %"] = (
        df["Course Qualified"]
        / df["Held Strength"]
        * 100
    ).round(1)

    df["Cadre Qualification %"] = (
        df["Cadre Qualified"]
        / df["Held Strength"]
        * 100
    ).round(1)

    df["Promotion Coverage %"] = (
        df["Vacancies in Next Rank"]
        / df["Eligible for Next Rank"]
        * 100
    ).round(1)

    # ====================================
    # FILTERS
    # ====================================

    selected_ranks = st.multiselect(
        "Ranks",
        options=df["Rank"].unique(),
        default=df["Rank"].unique()
    )

    filtered_df = df[
        df["Rank"].isin(selected_ranks)
    ]

    # ====================================
    # KPIs
    # ====================================

    total_strength = (
        filtered_df["Held Strength"]
        .sum()
    )

    total_eligible = (
        filtered_df["Eligible for Next Rank"]
        .sum()
    )

    total_vacancies = (
        filtered_df["Vacancies in Next Rank"]
        .sum()
    )

    coverage = (
        total_vacancies
        / total_eligible
        * 100
        if total_eligible > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Held Strength",
        f"{total_strength:,.0f}"
    )

    c2.metric(
        "Eligible",
        f"{total_eligible:,.0f}"
    )

    c3.metric(
        "Vacancies",
        f"{total_vacancies:,.0f}"
    )

    c4.metric(
        "Coverage %",
        f"{coverage:.1f}%"
    )

    st.divider()

    # ====================================
    # CHARTS
    # ====================================

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df,
            x="Rank",
            y="Held Strength",
            title="Held Strength by Rank"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            filtered_df,
            x="Rank",
            y=[
                "Eligible for Next Rank",
                "Vacancies in Next Rank"
            ],
            barmode="group",
            title="Eligibility vs Vacancies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df,
            x="Rank",
            y=[
                "Course Qualified",
                "Cadre Qualified"
            ],
            barmode="group",
            title="Qualification Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            filtered_df,
            x="Rank",
            y="Promotion Coverage %",
            text_auto=".1f",
            title="Promotion Coverage %"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader(
        "Promotion Readiness Matrix"
    )

    readiness_cols = [
        "Rank",
        "Course Qualification %",
        "Cadre Qualification %",
        "Promotion Coverage %"
    ]

    st.dataframe(
        filtered_df[readiness_cols]
        .style.background_gradient()
    )

    st.divider()

    with st.expander(
        "Detailed Promotion Data"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )