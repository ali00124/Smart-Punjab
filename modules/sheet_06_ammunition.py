import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import load_sheet
from utils.kpi_utils import calculate_percentage


def render_ammunition_state():
    
    st.title('SMART DASHBOARD')

    # ==================================================
    # LOAD SHEET
    # ==================================================

    sheet = load_sheet("6. Ammunition State")

    page_title = str(sheet.iloc[0, 0]).strip()

    # ==================================================
    # TABLE 1
    # ==================================================

    table1_title = str(sheet.iloc[3, 0]).strip()

    headers1 = sheet.iloc[4].tolist()

    df1 = sheet.iloc[5:9].copy()

    df1.columns = headers1

    # ==================================================
    # TABLE 2
    # ==================================================

    table2_title = str(sheet.iloc[10, 0]).strip()

    headers2 = sheet.iloc[11].tolist()

    df2 = sheet.iloc[12:18].copy()

    df2.columns = headers2

    # ==================================================
    # CLEANING
    # ==================================================

    def clean_df(df):

        numeric_cols = [
            "Authorized",
            "Held",
            "Deficiency",
            "First Line",
            "Second Line / Reserve"
        ]

        for col in numeric_cols:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df["Held %"] = (
            df["Held %"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

        return df

    df1 = clean_df(df1)
    df2 = clean_df(df2)

    # ==================================================
    # PAGE HEADER
    # ==================================================

    st.header("💣 Ammunition State")

    #st.caption(page_title)

    # ==================================================
    # FILTERS
    # ==================================================

    #st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:

        selected_small = st.multiselect(
            "Small Arms Ammunition",
            options=df1["Ammunition Type"].unique(),
            default=df1["Ammunition Type"].unique()
        )

    with col2:

        selected_heavy = st.multiselect(
            "Heavy Weapons Ammunition",
            options=df2["Ammunition Type"].unique(),
            default=df2["Ammunition Type"].unique()
        )

    filtered_df1 = df1[
        df1["Ammunition Type"].isin(selected_small)
    ]

    filtered_df2 = df2[
        df2["Ammunition Type"].isin(selected_heavy)
    ]

    # ==================================================
    # GRAND TOTALS
    # ==================================================

    grand_authorized = (
        filtered_df1["Authorized"].sum()
        + filtered_df2["Authorized"].sum()
    )

    grand_held = (
        filtered_df1["Held"].sum()
        + filtered_df2["Held"].sum()
    )

    grand_deficiency = (
        filtered_df1["Deficiency"].sum()
        + filtered_df2["Deficiency"].sum()
    )

    grand_firstline = (
        filtered_df1["First Line"].sum()
        + filtered_df2["First Line"].sum()
    )

    grand_reserve = (
        filtered_df1["Second Line / Reserve"].sum()
        + filtered_df2["Second Line / Reserve"].sum()
    )

    grand_held_pct = calculate_percentage(
        grand_held,
        grand_authorized
    )

    # ==================================================
    # OVERALL KPIs
    # ==================================================

    st.subheader("Overall Ammunition Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Authorized",
        f"{grand_authorized:,.0f}"
    )

    c2.metric(
        "Held",
        f"{grand_held:,.0f}"
    )

    c3.metric(
        "Held %",
        f"{grand_held_pct:.1f}%"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Deficiency",
        f"{grand_deficiency:,.0f}"
    )

    c5.metric(
        "First Line",
        f"{grand_firstline:,.0f}"
    )

    c6.metric(
        "Reserve",
        f"{grand_reserve:,.0f}"
    )

    # ==================================================
    # STOCK DISTRIBUTION
    # ==================================================

    st.divider()

    stock_df = pd.DataFrame({

        "Type": [
            "First Line",
            "Reserve"
        ],

        "Quantity": [
            grand_firstline,
            grand_reserve
        ]
    })

    fig = px.pie(
        stock_df,
        names="Type",
        values="Quantity",
        title="Stock Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # TABLE 1 SECTION
    # ==================================================

    st.divider()

    st.subheader(table1_title)

    auth = filtered_df1["Authorized"].sum()
    held = filtered_df1["Held"].sum()
    deficiency = filtered_df1["Deficiency"].sum()
    firstline = filtered_df1["First Line"].sum()
    reserve = filtered_df1["Second Line / Reserve"].sum()

    held_pct = calculate_percentage(
        held,
        auth
    )

    cols = st.columns(6)

    cols[0].metric("Authorized", f"{auth:,.0f}")
    cols[1].metric("Held", f"{held:,.0f}")
    cols[2].metric("Held %", f"{held_pct:.1f}%")
    cols[3].metric("Deficiency", f"{deficiency:,.0f}")
    cols[4].metric("First Line", f"{firstline:,.0f}")
    cols[5].metric("Reserve", f"{reserve:,.0f}")

    #left, right = st.columns(2)
    left, = st.columns(1)
    
    with left:

        fig = px.bar(
            filtered_df1,
            x="Ammunition Type",
            y=["Authorized", "Held"],
            barmode="group",
            title="Authorized vs Held"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    '''with right:

        fig = px.bar(
            filtered_df1,
            x="Ammunition Type",
            y=[
                "First Line",
                "Second Line / Reserve"
            ],
            barmode="stack",
            title="Stock Composition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )'''

    '''left, right = st.columns(2)

    with left:

        fig = px.bar(
            filtered_df1,
            x="Ammunition Type",
            y="Held %",
            text_auto=".1f",
            title="Held Percentage"
        )

        fig.add_hline(y=80)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            filtered_df1.sort_values(
                "Deficiency",
                ascending=False
            ),
            x="Ammunition Type",
            y="Deficiency",
            text_auto=True,
            title="Deficiency Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with st.expander("Small Arms Ammunition Data"):

        st.dataframe(
            filtered_df1,
            use_container_width=True,
            hide_index=True
        )'''

    # ==================================================
    # TABLE 2 SECTION
    # ==================================================

    st.divider()

    st.subheader(table2_title)

    auth = filtered_df2["Authorized"].sum()
    held = filtered_df2["Held"].sum()
    deficiency = filtered_df2["Deficiency"].sum()
    firstline = filtered_df2["First Line"].sum()
    reserve = filtered_df2["Second Line / Reserve"].sum()

    held_pct = calculate_percentage(
        held,
        auth
    )

    cols = st.columns(6)

    cols[0].metric("Authorized", f"{auth:,.0f}")
    cols[1].metric("Held", f"{held:,.0f}")
    cols[2].metric("Held %", f"{held_pct:.1f}%")
    cols[3].metric("Deficiency", f"{deficiency:,.0f}")
    cols[4].metric("First Line", f"{firstline:,.0f}")
    cols[5].metric("Reserve", f"{reserve:,.0f}")

    #left, right = st.columns(2)
    left, = st.columns(1)

    with left:

        fig = px.bar(
            filtered_df2,
            x="Ammunition Type",
            y=["Authorized", "Held"],
            barmode="group",
            title="Authorized vs Held"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    '''with right:

        fig = px.bar(
            filtered_df2,
            x="Ammunition Type",
            y=[
                "First Line",
                "Second Line / Reserve"
            ],
            barmode="stack",
            title="Stock Composition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )'''

    '''left, right = st.columns(2)

    with left:

        fig = px.bar(
            filtered_df2,
            x="Ammunition Type",
            y="Held %",
            text_auto=".1f",
            title="Held Percentage"
        )

        fig.add_hline(y=80)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            filtered_df2.sort_values(
                "Deficiency",
                ascending=False
            ),
            x="Ammunition Type",
            y="Deficiency",
            text_auto=True,
            title="Deficiency Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )'''

    '''with st.expander("Heavy Weapons Ammunition Data"):

        st.dataframe(
            filtered_df2,
            use_container_width=True,
            hide_index=True
        )'''
        
    st.subheader("Heavy Weapons Ammunition Data")
    
    st.dataframe(
        filtered_df2,
        use_container_width=True,
        hide_index=True
    )