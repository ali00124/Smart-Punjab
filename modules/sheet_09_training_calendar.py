import streamlit as st
import pandas as pd
import plotly.express as px
import re

from utils.excel_loader import (
    load_sheet,
    clean_column_names
)


def parse_dates(date_str):

    date_str = str(date_str).strip()

    try:

        if "-" in date_str:

            match = re.match(
                r"(\d+)-(\d+)\s+([A-Za-z]+)\s+(\d+)",
                date_str
            )

            if match:

                start_day = match.group(1)
                end_day = match.group(2)
                month = match.group(3)
                year = match.group(4)

                start = pd.to_datetime(
                    f"{start_day} {month} {year}"
                )

                end = pd.to_datetime(
                    f"{end_day} {month} {year}"
                )

                return start, end

        else:

            dt = pd.to_datetime(
                date_str,
                dayfirst=True
            )

            return dt, dt

    except:

        return pd.NaT, pd.NaT

    return pd.NaT, pd.NaT


def render_training_calendar():

    sheet = load_sheet(
        "9. Upcoming Events"
    )

    title = str(
        sheet.iloc[0, 0]
    ).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:14].copy()

    df.columns = headers

    df = clean_column_names(df)

    st.header(
        "📅 Upcoming Major Events / Training Calendar"
    )

    st.caption(title)

    # =====================================
    # DATE PROCESSING
    # =====================================

    starts = []
    ends = []

    for value in df["Dates"]:

        start, end = parse_dates(value)

        starts.append(start)
        ends.append(end)

    df["Start Date"] = starts
    df["End Date"] = ends

    df["Duration"] = (
        df["End Date"] -
        df["Start Date"]
    ).dt.days + 1

    df["Month"] = (
        df["Start Date"]
        .dt.strftime("%b %Y")
    )

    # =====================================
    # FILTERS
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        selected_types = st.multiselect(
            "Event Type",
            options=df["Type"].unique(),
            default=df["Type"].unique()
        )

    with col2:

        selected_months = st.multiselect(
            "Month",
            options=df["Month"].unique(),
            default=df["Month"].unique()
        )

    filtered_df = df[
        (df["Type"].isin(selected_types))
        &
        (df["Month"].isin(selected_months))
    ]

    # =====================================
    # KPIs
    # =====================================

    total_events = len(filtered_df)

    next_event = (
        filtered_df
        .sort_values("Start Date")
        .iloc[0]["Event / Activity"]
        if len(filtered_df)
        else "N/A"
    )

    training_count = (
        filtered_df["Type"]
        .astype(str)
        .str.contains("Training")
        .sum()
    )

    inspection_count = (
        filtered_df["Type"]
        .astype(str)
        .str.contains("Inspection")
        .sum()
    )

    field_ex_count = (
        filtered_df["Type"]
        .astype(str)
        .str.contains("Field")
        .sum()
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Events",
        total_events
    )

    c2.metric(
        "Training",
        training_count
    )

    c3.metric(
        "Field Ex",
        field_ex_count
    )

    c4.metric(
        "Inspection",
        inspection_count
    )

    c5.metric(
        "Next Event",
        next_event
    )

    # =====================================
    # TIMELINE
    # =====================================

    st.divider()

    fig = px.timeline(
        filtered_df,
        x_start="Start Date",
        x_end="End Date",
        y="Event / Activity",
        color="Type",
        title="Training Timeline"
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # EVENT TYPE DISTRIBUTION
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            filtered_df,
            names="Type",
            title="Event Types"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        month_df = (
            filtered_df
            .groupby("Month")
            .size()
            .reset_index(name="Events")
        )

        fig = px.bar(
            month_df,
            x="Month",
            y="Events",
            title="Events By Month"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================
    # DURATION ANALYSIS
    # =====================================

    st.divider()

    fig = px.bar(
        filtered_df,
        x="Event / Activity",
        y="Duration",
        title="Event Duration (Days)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # DATA TABLE
    # =====================================

    st.divider()

    with st.expander(
        "Detailed Training Schedule"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )