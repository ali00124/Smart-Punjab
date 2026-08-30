import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import load_sheet, clean_column_names


def render_audit_objections():
    
    

    # ==========================================
    # LOAD SHEET
    # ==========================================

    sheet = load_sheet("8. Audit Objections")

    title = str(sheet.iloc[0, 0]).strip()

    headers = sheet.iloc[3].tolist()

    df = sheet.iloc[4:7].copy()

    df.columns = headers

    df = clean_column_names(df)

    # ==========================================
    # CLEAN DATA
    # ==========================================

    df["No. of Objections"] = pd.to_numeric(
        df["No. of Objections"],
        errors="coerce"
    )

    df["Amount Involved (PKR)"] = (
        df["Amount Involved (PKR)"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["Amount Involved (PKR)"] = pd.to_numeric(
        df["Amount Involved (PKR)"],
        errors="coerce"
    )

    # ==========================================
    # HEADER
    # ==========================================

    st.header("📋 Remaining Audit Objections")

    #st.caption(title)

    # ==========================================
    # FILTER
    # ==========================================

    selected_category = st.multiselect(
        "Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        df["Category"].isin(selected_category)
    ]

    # ==========================================
    # KPIs
    # ==========================================

    total_objections = filtered_df[
        "No. of Objections"
    ].sum()

    total_amount = filtered_df[
        "Amount Involved (PKR)"
    ].sum()

    avg_amount = (
        total_amount / total_objections
        if total_objections > 0
        else 0
    )

    oldest_pending = filtered_df[
        "Oldest Pending Since"
    ].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Objections",
        f"{total_objections:,}"
    )

    c2.metric(
        "Amount Involved",
        f"PKR {total_amount:,.0f}"
    )

    c3.metric(
        "Avg Amount / Objection",
        f"PKR {avg_amount:,.0f}"
    )

    c4.metric(
        "Oldest Pending",
        str(oldest_pending)
    )

    st.divider()

    # ==========================================
    # CHARTS
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            filtered_df,
            x="Category",
            y="No. of Objections",
            text_auto=True,
            title="Objections by Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            filtered_df,
            x="Category",
            y="Amount Involved (PKR)",
            text_auto=True,
            title="Financial Exposure"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    '''st.divider()

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            filtered_df,
            names="Category",
            values="No. of Objections",
            title="Objection Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.pie(
            filtered_df,
            names="Category",
            values="Amount Involved (PKR)",
            title="Exposure Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    fig = px.scatter(
        filtered_df,
        x="No. of Objections",
        y="Amount Involved (PKR)",
        size="Amount Involved (PKR)",
        hover_name="Category",
        title="Risk Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )'''

    st.divider()

    '''with st.expander(
        "Detailed Audit Objections"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )'''
        
    st.subheader("Detailed Audit Objections")
    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )