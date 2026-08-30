import streamlit as st
import pandas as pd
import plotly.express as px
import re

from utils.excel_loader import (
    load_sheet,
    clean_column_names
)


def duration_to_months(text):

    text = str(text).lower()

    years = 0
    months = 0

    yr = re.search(r'(\d+)\s*yr', text)
    mo = re.search(r'(\d+)\s*mo', text)

    if yr:
        years = int(yr.group(1))

    if mo:
        months = int(mo.group(1))

    return years * 12 + months


def officer_category(appt):

    appt = str(appt).lower()

    if "commanding officer" in appt:
        return "Command"

    if "2ic" in appt:
        return "Command"

    if "coy" in appt:
        return "Company Commander"

    return "Staff Officer"


def render_officers():
    
    

    sheet = load_sheet(
        "11. Officers Appointments"
    )

    title = str(
        sheet.iloc[0, 0]
    ).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:15].copy()

    df.columns = headers

    df = clean_column_names(df)

    st.header("Officers – Key Appointments")

    #st.caption(title)

    # =====================================
    # DERIVED COLUMNS
    # =====================================

    df["Duration Months"] = (
        df["Duration in Appt"]
        .apply(duration_to_months)
    )

    df["Category"] = (
        df["Appointment"]
        .apply(officer_category)
    )

    # =====================================
    # FILTERS
    # =====================================

    selected_category = st.multiselect(
        "Officer Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        df["Category"].isin(
            selected_category
        )
    ]

    # =====================================
    # KPIs
    # =====================================

    total_officers = len(filtered_df)

    avg_duration = round(
        filtered_df[
            "Duration Months"
        ].mean(),
        1
    )

    company_commanders = len(
        filtered_df[
            filtered_df["Category"]
            == "Company Commander"
        ]
    )

    staff_officers = len(
        filtered_df[
            filtered_df["Category"]
            == "Staff Officer"
        ]
    )

    c1, c3, c4 = st.columns(3)

    c1.metric(
        "Total Officers",
        total_officers
    )

    '''c2.metric(
        "Avg Duration",
        f"{avg_duration} Months"
    )'''

    c3.metric(
        "Coy Commanders",
        company_commanders
    )

    c4.metric(
        "Staff Officers",
        staff_officers
    )

    st.divider()

    # =====================================
    # CHARTS
    # =====================================

    #col1, col2 = st.columns(2)
    col2, = st.columns(1)
    
    '''with col1:

        fig = px.pie(
            filtered_df,
            names="Category",
            title="Officer Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )'''

    with col2:

        fig = px.bar(
            filtered_df,
            x="Appointment",
            y="Duration Months",
            title="Duration in Appointment"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    '''st.divider()

    fig = px.bar(
        filtered_df.sort_values(
            "Duration Months",
            ascending=False
        ),
        x="Rank & Name",
        y="Duration Months",
        title="Officer Experience Ranking"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )'''

    st.divider()

    st.subheader(
        "Officer Directory"
    )

    display_cols = [
        "Appointment",
        "Rank & Name",
        "Army No.",
        "Contact (Ext)",
        "Additional Tasks / Responsibilities",
        "Remarks"
    ]

    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True,
            hide_index=True
    )