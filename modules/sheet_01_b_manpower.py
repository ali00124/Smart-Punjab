import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.excel_loader import load_sheet


def render_manpower():

    sheet = load_sheet("1. Combat Potential")

    # ==================================================
    # HEADER
    # ==================================================

    st.title("SMART DASHBOARD")
    st.header(
            "👥 Manpower Strength State"
        )

    # ==================================================
    # MANPOWER TABLE
    # ==================================================

    manpower_headers = [
        str(x).strip()
        for x in sheet.iloc[16].tolist()
    ]

    manpower_df = sheet.iloc[17:29].copy()

    manpower_df.columns = manpower_headers

    manpower_df = manpower_df.loc[
        :,
        ~pd.isna(manpower_df.columns)
    ]

    manpower_df = manpower_df.dropna(
        axis=1,
        how="all"
    )

    manpower_df.columns = (
        manpower_df.columns
        .astype(str)
        .str.strip()
    )

    manpower_df["Strength"] = pd.to_numeric(
        manpower_df["Strength"],
        errors="coerce"
    )

    def pct_to_float(value):

        if pd.isna(value):
            return 0

        if isinstance(value, (int, float)):
            if value <= 1:
                return value * 100
            return float(value)

        return float(
            str(value)
            .replace("%", "")
            .strip()
        )

    
    available = int(
        manpower_df.loc[
            manpower_df["Category"]
            == "AVAILABLE MANPOWER",
            "Strength"
        ].iloc[0]
    )

    st.divider()
    
    c1, = st.columns(1)
    
    c1.metric(
        "Available Manpower",
        available
    )
        
    # ==================================================
    # MANPOWER TABLE
    # ==================================================

    manpower_headers = [
        str(x).strip()
        for x in sheet.iloc[16].tolist()
    ]

    manpower_df = sheet.iloc[17:29].copy()

    manpower_df.columns = manpower_headers

    manpower_df = manpower_df.loc[
        :,
        ~pd.isna(manpower_df.columns)
    ]

    manpower_df = manpower_df.dropna(
        axis=1,
        how="all"
    )

    manpower_df.columns = (
        manpower_df.columns
        .astype(str)
        .str.strip()
    )

    manpower_df["Strength"] = pd.to_numeric(
        manpower_df["Strength"],
        errors="coerce"
    )

    # ==================================================
    # MANPOWER KPIs
    # ==================================================

    authorized = int(
        manpower_df.loc[
            manpower_df["Category"]
            == "AUTHORIZED STRENGTH",
            "Strength"
        ].iloc[0]
    )

    held = int(
        manpower_df.loc[
            manpower_df["Category"]
            == "HELD STRENGTH",
            "Strength"
        ].iloc[0]
    )

    available = int(
        manpower_df.loc[
            manpower_df["Category"]
            == "AVAILABLE MANPOWER",
            "Strength"
        ].iloc[0]
    )

    deficiency = authorized - held


    # ==================================================
    # MANPOWER SECTION
    # ==================================================

    st.divider()

    

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Authorized",
        authorized
    )

    m2.metric(
        "Held",
        held
    )

    m3.metric(
        "Available",
        available
    )

    m4.metric(
        "Deficiency",
        deficiency
    )

    # ==================================================
    # MANPOWER COMPOSITION
    # ==================================================

    absence_df = manpower_df[
        manpower_df["Category"].isin([
            "On Privilege Leave (P Leave)",
            "On Casual Leave (C Leave)",
            "Formation Guard Duties",
            "Out Station Guard Duties",
            "Attachments in Various HQs",
            "On Various Courses"
        ])
    ].copy()

    away_strength = (
        absence_df["Strength"]
        .fillna(0)
        .sum()
    )

    manpower_comp = pd.DataFrame({
        "Category": [
            "Available",
            "Away",
            "Deficiency"
        ],
        "Strength": [
            available,
            away_strength,
            deficiency
        ]
    })

    left, right = st.columns(2)

    with left:

        fig = px.pie(
            manpower_comp,
            names="Category",
            values="Strength",
            hole=0.45,
            title="Manpower Composition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        personnel_df = pd.DataFrame({
            "Stage": [
                "Authorized",
                "Held",
                "Available"
            ],
            "Strength": [
                authorized,
                held,
                available
            ]
        })

        fig = px.bar(
            personnel_df,
            x="Stage",
            y="Strength",
            text_auto=True,
            title="Personnel Availability"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # DETAILED TABLES
    # ==================================================

    '''with st.expander(
        "👥 Manpower Details"
    ):
        st.dataframe(
            manpower_df,
            use_container_width=True,
            hide_index=True
        )'''
        
    st.subheader("Manpower Details")
    
    for col in ['% of Held', '% of Authorized']:
        manpower_df.iloc[1:, manpower_df.columns.get_loc(col)] = (pd.to_numeric(manpower_df.iloc[1:][col].astype(str).str.replace(r'[%\-]', '', regex=True).str.strip(), errors='coerce') * 100).round(1)
    
    for col in ['% of Held', '% of Authorized']:
        manpower_df[col] = manpower_df[col].apply(
            lambda x: str(x) if pd.notna(x) else x
        ).apply(
            lambda x: x if str(x).strip().endswith('%') else f"{str(x).strip()}%"
        )
        
    for col in ['% of Held', '% of Authorized']:
        manpower_df[col] = manpower_df[col].replace('nan%', None)
        
    manpower_df = manpower_df[manpower_df['Category'].notna()].reset_index(drop=True)
    
    
    st.dataframe(
        manpower_df,
        use_container_width=True,
        hide_index=True
    )