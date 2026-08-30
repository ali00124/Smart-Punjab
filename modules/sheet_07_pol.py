import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import load_sheet, clean_column_names
from utils.kpi_utils import calculate_percentage


def render_pol_state():
    
    

    # ==================================================
    # LOAD SHEET
    # ==================================================

    sheet = load_sheet("7. POL State")

    title = str(sheet.iloc[0, 0]).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:7].copy()

    df.columns = headers
    df = clean_column_names(df)
    
    #st.write("Headers found:")

    summary = sheet.iloc[7]

    # ==================================================
    # CLEAN DATA
    # ==================================================

    numeric_cols = [
    col
    for col in [
        "Held Quantity (Litres)",
        "Authorized / Entitlement",
        "Balance / Deficiency"
    ]
    if col in df.columns
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

    # ==================================================
    # CALCULATED METRICS
    # ==================================================

    df["Stock %"] = (
        df["Held Quantity (Litres)"]
        / df["Authorized / Entitlement"]
        * 100
    ).round(1)

    # ==================================================
    # HEADER
    # ==================================================

    st.header("⛽ POL State")

    #st.caption(title)

    # ==================================================
    # FILTER
    # ==================================================

    selected_categories = st.multiselect(
        "POL Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        df["Category"].isin(
            selected_categories
        )
    ]

    # ==================================================
    # KPIs
    # ==================================================

    total_held = filtered_df[
        "Held Quantity (Litres)"
    ].sum()

    total_authorized = filtered_df[
        "Authorized / Entitlement"
    ].sum()

    total_deficiency = filtered_df[
        "Balance / Deficiency"
    ].sum()

    stock_pct = calculate_percentage(
        total_held,
        total_authorized
    )

    st.subheader("POL Readiness Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Held (Litres)",
        f"{total_held:,.0f}"
    )

    c2.metric(
        "Entitlement",
        f"{total_authorized:,.0f}"
    )

    c3.metric(
        "Deficiency",
        f"{total_deficiency:,.0f}"
    )

    c4.metric(
        "Stock %",
        f"{stock_pct:.1f}%"
    )

    # ==================================================
    # CHART 1
    # ==================================================

    st.divider()

    fig = px.bar(
        filtered_df,
        x="Category",
        y="Held Quantity (Litres)",
        title="Held Quantity by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # CHART 2
    # ==================================================

    '''fig = px.bar(
        filtered_df.sort_values(
            "Balance / Deficiency",
            ascending=False
        ),
        x="Category",
        y="Balance / Deficiency",
        text_auto=True,
        title="POL Deficiency Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # CHART 3
    # ==================================================

    fig = px.bar(
        filtered_df,
        x="Category",
        y="Stock %",
        text_auto=".1f",
        title="Stock Percentage"
    )

    fig.add_hline(
        y=80,
        line_dash="dash"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )'''

    # ==================================================
    # CHART 4
    # ==================================================

    distribution_df = pd.DataFrame({
        "Category": filtered_df["Category"],
        "Held": filtered_df["Held Quantity (Litres)"]
    })

    fig = px.pie(
        distribution_df,
        names="Category",
        values="Held",
        title="POL Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # CHART 5
    # ==================================================

    '''fig = px.scatter(
        filtered_df,
        x="Authorized / Entitlement",
        y="Held Quantity (Litres)",
        size="Held Quantity (Litres)",
        hover_name="Category",
        title="POL Readiness Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )'''

    # ==================================================
    # DETAIL TABLE
    # ==================================================

    st.divider()

    '''with st.expander("Detailed POL Data"):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )'''
        
    st.subheader("Detailed POL Data")
    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )