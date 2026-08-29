import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import load_sheet
from utils.kpi_utils import calculate_percentage


def render_critical_equipment():
    
    st.title('SMART DASHBOARD')

    # ==================================================
    # LOAD SHEET
    # ==================================================

    sheet = load_sheet("4. Critical Equipment")

    # ==================================================
    # EXTRACT DATA
    # ==================================================

    title = str(sheet.iloc[0, 0]).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:13].copy()

    df.columns = headers

    summary = sheet.iloc[13]

    # ==================================================
    # CLEAN DATA
    # ==================================================

    numeric_cols = [
        "Authorized",
        "Held",
        "Serviceable",
        "Unserviceable"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Held %

    if df["Held %"].astype(str).str.contains("%").any():

        df["Held %"] = (
            df["Held %"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

    else:

        df["Held %"] = (
            pd.to_numeric(
                df["Held %"],
                errors="coerce"
            ) * 100
        )

    # Serviceability %

    if df["Serviceability %"].astype(str).str.contains("%").any():

        df["Serviceability %"] = (
            df["Serviceability %"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

    else:

        df["Serviceability %"] = (
            pd.to_numeric(
                df["Serviceability %"],
                errors="coerce"
            ) * 100
        )

    # ==================================================
    # TITLE
    # ==================================================

    st.header("🔭 Critical Equipment State")

    #st.caption(title)

    # ==================================================
    # FILTER
    # ==================================================

    selected_equipment = st.multiselect(
        "Equipment Type",
        options=df["Equipment Type"].unique(),
        default=df["Equipment Type"].unique()
    )

    filtered_df = df[
        df["Equipment Type"].isin(
            selected_equipment
        )
    ]

    # ==================================================
    # KPI CALCULATIONS
    # ==================================================

    authorized = filtered_df["Authorized"].sum()

    held = filtered_df["Held"].sum()

    serviceable = filtered_df["Serviceable"].sum()

    unserviceable = filtered_df["Unserviceable"].sum()

    held_pct = calculate_percentage(
        held,
        authorized
    )

    serviceability_pct = calculate_percentage(
        serviceable,
        held
    )

    # ==================================================
    # KPIs
    # ==================================================

    st.subheader("Equipment Readiness Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Authorized",
        f"{authorized:,}"
    )

    c2.metric(
        "Held",
        f"{held:,}"
    )

    c3.metric(
        "Held %",
        f"{held_pct:.1f}%"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Serviceable",
        f"{serviceable:,}"
    )

    c5.metric(
        "Unserviceable",
        f"{unserviceable:,}"
    )

    c6.metric(
        "Serviceability %",
        f"{serviceability_pct:.1f}%"
    )

    # ==================================================
    # AUTHORIZED VS HELD
    # ==================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df,
            x="Equipment Type",
            y=[
                "Authorized",
                "Held"
            ],
            barmode="group",
            title="Authorized vs Held"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # SERVICEABLE VS UNSERVICEABLE
    # ==================================================

    with col2:

        fig = px.bar(
            filtered_df,
            x="Equipment Type",
            y=[
                "Serviceable",
                "Unserviceable"
            ],
            barmode="stack",
            title="Serviceable vs Unserviceable"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # HELD %
    # ==================================================

    '''st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df.sort_values(
                "Held %",
                ascending=False
            ),
            x="Equipment Type",
            y="Held %",
            title="Held Percentage",
            text_auto=".1f"
        )

        fig.add_hline(
            y=80,
            line_dash="dash"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # SERVICEABILITY %
    # ==================================================

    with col2:

        fig = px.bar(
            filtered_df.sort_values(
                "Serviceability %",
                ascending=False
            ),
            x="Equipment Type",
            y="Serviceability %",
            title="Serviceability Percentage",
            text_auto=".1f"
        )

        fig.add_hline(
            y=90,
            line_dash="dash"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # READINESS MATRIX
    # ==================================================

    st.divider()

    fig = px.scatter(
        filtered_df,
        x="Held %",
        y="Serviceability %",
        size="Held",
        hover_name="Equipment Type",
        title="Equipment Readiness Matrix"
    )

    fig.add_vline(
        x=80,
        line_dash="dash"
    )

    fig.add_hline(
        y=90,
        line_dash="dash"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # PIE CHART
    # ==================================================

    readiness_df = pd.DataFrame({

        "Status": [
            "Serviceable",
            "Unserviceable"
        ],

        "Count": [
            serviceable,
            unserviceable
        ]
    })

    fig = px.pie(
        readiness_df,
        names="Status",
        values="Count",
        title="Equipment Condition Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )'''

    # ==================================================
    # DATA TABLE
    # ==================================================

    st.divider()

    '''with st.expander(
        "Detailed Equipment Data"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )'''
        
    st.subheader("Detailed Equipment Data")
    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )