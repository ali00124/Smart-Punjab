import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.excel_loader import load_sheet


def render_combat_potential():

    sheet = load_sheet("1. Combat Potential")

    # ==================================================
    # HEADER
    # ==================================================

    unit_info = str(sheet.iloc[1, 0])

    st.title("SMART DASHBOARD")
    #st.caption(unit_info)

    # ==================================================
    # COMBAT POTENTIAL TABLE
    # ==================================================

    combat_headers = [
        str(x).strip()
        for x in sheet.iloc[4].tolist()
    ]

    combat_df = sheet.iloc[5:12].copy()
    combat_df.columns = combat_headers

    combat_df = combat_df.dropna(
        axis=1,
        how="all"
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

    combat_df["Availability %"] = (
        combat_df["Availability %"]
        .apply(pct_to_float)
    )

    combat_df["Weightage"] = (
        combat_df["Weightage"]
        .apply(pct_to_float)
    )

    combat_df["Weighted Score"] = (
        combat_df["Weighted Score"]
        .apply(pct_to_float)
    )

    overall_combat_potential = pct_to_float(
        sheet.iloc[12, 5]
    )

    # ==================================================
    # STATUS
    # ==================================================

    if overall_combat_potential >= 75:
        readiness_status = "🟢 High Readiness"
        status_color = "green"

    elif overall_combat_potential >= 60:
        readiness_status = "🟡 Moderate Readiness"
        status_color = "orange"

    else:
        readiness_status = "🔴 Low Readiness"
        status_color = "red"

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
    # TOP KPIs
    # ==================================================

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Combat Potential",
        f"{overall_combat_potential:.1f}%"
    )

    c2.metric(
        "Target",
        "75%"
    )

    c3.metric(
        "Gap",
        f"{75 - overall_combat_potential:.1f}%"
    )

    c4.metric(
        "Available Manpower",
        available
    )

    # ==================================================
    # GAUGE
    # ==================================================

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=overall_combat_potential,
            number={"suffix": "%"},
            title={
                "text":
                "Overall Combat Potential"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 60],
                        "color": "#ffcccc"
                    },
                    {
                        "range": [60, 75],
                        "color": "#fff2cc"
                    },
                    {
                        "range": [75, 100],
                        "color": "#d9ead3"
                    }
                ],
                "threshold": {
                    "line": {
                        "width": 4
                    },
                    "value": 75
                }
            }
        )
    )

    gauge.update_layout(
        height=420
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # ==================================================
    # COMBAT CHARTS
    # ==================================================

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            combat_df,
            x="Parameter",
            y="Availability %",
            title="Availability by Parameter",
            text_auto=".1f"
        )

        fig.add_hline(
            y=75,
            line_dash="dash"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="%"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            combat_df,
            x="Parameter",
            y="Weighted Score",
            title="Contribution to Combat Potential",
            text_auto=".1f"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="%"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # MANPOWER SECTION
    # ==================================================

    st.divider()

    st.subheader(
        "👥 Manpower Strength State"
    )

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

    with st.expander(
        "📊 Combat Potential Details"
    ):
        st.dataframe(
            combat_df,
            use_container_width=True
        )

    with st.expander(
        "👥 Manpower Details"
    ):
        st.dataframe(
            manpower_df,
            use_container_width=True
        )