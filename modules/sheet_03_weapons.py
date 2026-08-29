import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import load_sheet
from utils.kpi_utils import calculate_percentage


def render_weapons_state():
    
    st.title('SMART DASHBOARD')

    # ==================================================
    # LOAD SHEET
    # ==================================================

    sheet = load_sheet("3. Weapons State")

    # ==================================================
    # EXTRACT DATA
    # ==================================================

    title = str(sheet.iloc[0, 0]).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:15].copy()

    df.columns = headers

    summary = sheet.iloc[15]

    # ==================================================
    # CLEAN DATA
    # ==================================================

    numeric_cols = [
        "Authorized",
        "Held",
        "Deficiency",
        "Cl-1 (S)",
        "Cl-2 (S)",
        "Cl-3 (S)",
        "Cl-4 (WS)",
        "Cl-5/6 (Condemn)"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Held % can be either 0.933 or 93.3%
    try:

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

    except Exception:

        df["Held %"] = pd.to_numeric(
            df["Held %"],
            errors="coerce"
        )

    # ==================================================
    # PAGE TITLE
    # ==================================================

    st.header("🔫 Weapons State")

    st.caption(title)

    # ==================================================
    # FILTER
    # ==================================================

    selected_weapons = st.multiselect(
        "Weapon Type",
        options=df["Weapon Type"].unique(),
        default=df["Weapon Type"].unique()
    )

    filtered_df = df[
        df["Weapon Type"].isin(selected_weapons)
    ]

    # ==================================================
    # KPI CALCULATIONS
    # ==================================================

    authorized = filtered_df["Authorized"].sum()

    held = filtered_df["Held"].sum()

    deficiency = filtered_df["Deficiency"].sum()

    held_pct = calculate_percentage(
        held,
        authorized
    )

    class1 = filtered_df["Cl-1 (S)"].sum()

    class2 = filtered_df["Cl-2 (S)"].sum()

    class3 = filtered_df["Cl-3 (S)"].sum()

    class4 = filtered_df["Cl-4 (WS)"].sum()

    class56 = filtered_df["Cl-5/6 (Condemn)"].sum()

    # ==================================================
    # KPI SECTION
    # ==================================================

    st.subheader("Weapons Readiness Summary")

    c1, c2, c3, c4 = st.columns(4)

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

    c4.metric(
        "Deficiency",
        f"{deficiency:,}"
    )

    c5, c6, c7, c8, c9 = st.columns(5)

    c5.metric(
        "Class 1",
        f"{class1:,}"
    )

    c6.metric(
        "Class 2",
        f"{class2:,}"
    )

    c7.metric(
        "Class 3",
        f"{class3:,}"
    )

    c8.metric(
        "Class 4",
        f"{class4:,}"
    )

    c9.metric(
        "Class 5/6",
        f"{class56:,}"
    )

    # ==================================================
    # AUTHORIZED VS HELD
    # ==================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df,
            x="Weapon Type",
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
    # HELD %
    # ==================================================

    with col2:

        fig = px.bar(
            filtered_df.sort_values(
                "Held %",
                ascending=False
            ),
            x="Weapon Type",
            y="Held %",
            title="Held Percentage",
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
    # CONDITION CLASSIFICATION
    # ==================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df,
            x="Weapon Type",
            y=[
                "Cl-1 (S)",
                "Cl-2 (S)",
                "Cl-3 (S)",
                "Cl-4 (WS)",
                "Cl-5/6 (Condemn)"
            ],
            barmode="stack",
            title="Condition Classification"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # DEFICIENCY ANALYSIS
    # ==================================================

    with col2:

        fig = px.bar(
            filtered_df.sort_values(
                "Deficiency",
                ascending=False
            ),
            x="Weapon Type",
            y="Deficiency",
            title="Deficiency Analysis",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # CONDITION DISTRIBUTION
    # ==================================================

    st.divider()

    condition_df = pd.DataFrame({
        "Condition": [
            "Class 1",
            "Class 2",
            "Class 3",
            "Class 4",
            "Class 5/6"
        ],
        "Count": [
            class1,
            class2,
            class3,
            class4,
            class56
        ]
    })

    fig = px.pie(
        condition_df,
        names="Condition",
        values="Count",
        title="Condition Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # DETAILED DATA
    # ==================================================

    st.divider()

    with st.expander("Detailed Weapons Data"):

        st.dataframe(
            filtered_df,
            use_container_width=True
        )