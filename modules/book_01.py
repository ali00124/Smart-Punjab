import streamlit as st
import pandas as pd
import plotly.express as px


def render_book1():
    
    

    # =====================================
    # LOAD EXCEL
    # =====================================

    df = pd.read_excel(
        "Book1.xlsx",
        header=None
    )

    # =====================================
    # DATA EXTRACTION
    # =====================================

    book1 = df.iloc[2:8, 0:15].copy()

    book1.columns = [
        "Rank",
        "Authorised",
        "Held",
        "Vacancies",
        "Vacancy %",
        "BCC",
        "SNC",
        "INC",
        "ALC",
        "Sub Prom Cadre",
        "Misc Courses",
        "Awards",
        "Red Ink Entry",
        "Matric",
        "FA"
    ]

    # =====================================
    # CLEAN DATA
    # =====================================

    for col in book1.columns[1:]:
        book1[col] = pd.to_numeric(
            book1[col],
            errors="coerce"
        ).fillna(0)

    # =====================================
    # KPIs
    # =====================================

    total_authorised = int(
        book1["Authorised"].sum()
    )

    total_held = int(
        book1["Held"].sum()
    )

    total_vacancies = int(
        book1["Vacancies"].sum()
    )

    vacancy_pct = (
        total_vacancies
        / total_authorised
        * 100
    )

    st.title("Promotions")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Authorised",
        total_authorised
    )

    k2.metric(
        "Held",
        total_held
    )

    k3.metric(
        "Vacancies",
        total_vacancies
    )

    k4.metric(
        "Vacancy %",
        f"{vacancy_pct:.1f}%"
    )

    st.divider()

    # =====================================
    # VACANCY ANALYSIS
    # =====================================

    #left, right = st.columns(2)
    left, = st.columns(1)

    with left:

        fig = px.bar(
            book1,
            x="Rank",
            y="Vacancies",
            text_auto=True,
            title="Vacancies by Rank"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    '''with right:

        fig = px.bar(
            book1,
            x="Rank",
            y="Vacancy %",
            text_auto=".1f",
            title="Vacancy % by Rank"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )'''

    # =====================================
    # QUALIFICATION DEFICIENCIES
    # =====================================

    st.subheader(
        "📚 Qualification Status"
    )

    qualification_cols = [
        "BCC",
        "SNC",
        "INC",
        "ALC",
        "Sub Prom Cadre",
        "Misc Courses"
    ]

    qualification_df = book1.melt(
        id_vars="Rank",
        value_vars=qualification_cols,
        var_name="Qualification",
        value_name="Count"
    )

    fig = px.bar(
        qualification_df,
        x="Rank",
        y="Count",
        color="Qualification",
        barmode="stack",
        title="Qualification Deficiencies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # DISCIPLINE / EDUCATION
    # =====================================

    '''left, right = st.columns(2)

    with left:

        fig = px.bar(
            book1,
            x="Rank",
            y=[
                "Awards",
                "Red Ink Entry"
            ],
            barmode="group",
            title="Awards vs Red Ink Entries"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            book1,
            x="Rank",
            y=[
                "Matric",
                "FA"
            ],
            barmode="group",
            title="Education Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )'''

    # =====================================
    # DETAIL TABLE
    # =====================================

    st.subheader("Detailed Promotion Data")

    st.dataframe(
        book1,
        use_container_width=True,
        hide_index=True
    )