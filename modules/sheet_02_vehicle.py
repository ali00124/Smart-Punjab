import streamlit as st
import pandas as pd
import plotly.express as px

from utils.excel_loader import load_sheet
from utils.kpi_utils import calculate_percentage


def render_vehicle_state():
    
    

    sheet = load_sheet("2. Vehicle State")

    # ==========================
    # TABLE A
    # ==========================

    title_a = str(sheet.iloc[3, 0]).strip()

    headers_a = sheet.iloc[4].tolist()

    df_a = sheet.iloc[5:8].copy()
    df_a.columns = headers_a

    # ==========================
    # TABLE B
    # ==========================

    title_b = str(sheet.iloc[10, 0]).strip()

    headers_b = sheet.iloc[11].tolist()

    df_b = sheet.iloc[12:18].copy()
    df_b.columns = headers_b

    # ==========================
    # GRAND TOTAL
    # ==========================

    grand_total = sheet.iloc[20]

    # ==========================
    # CLEANING
    # ==========================

    def clean_df(df):

        numeric_cols = [
            "Authorized",
            "Held",
            "On Road",
            "Off Road",
            "In Workshop",
            "Deficiency"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df["Serviceability %"] = (
            pd.to_numeric(
                df["Serviceability %"],
                errors="coerce"
            ) * 100
        )

        return df

    df_a = clean_df(df_a)
    df_b = clean_df(df_b)

    st.header("Vehicle State")

    # ==========================
    # OVERALL KPIs
    # ==========================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Authorized", int(grand_total[2]))
    c2.metric("Held", int(grand_total[3]))
    c3.metric("On Road", int(grand_total[4]))
    c4.metric(
        "Serviceability",
        f"{grand_total[7] * 100:.1f}%"
    )

    c5, c6, c7 = st.columns(3)

    c5.metric("Off Road", int(grand_total[5]))
    c6.metric("Workshop", int(grand_total[6]))
    c7.metric("Deficiency", int(grand_total[8]))

    # ==========================
    # FILTERS
    # ==========================

    st.divider()

    fa, fb = st.columns(2)

    with fa:

        selected_a = st.multiselect(
            "Tracked / Armoured",
            df_a["Type of Vehicle"].unique(),
            default=df_a["Type of Vehicle"].unique()
        )

    with fb:

        selected_b = st.multiselect(
            "Soft-Skin",
            df_b["Type of Vehicle"].unique(),
            default=df_b["Type of Vehicle"].unique()
        )

    filtered_a = df_a[
        df_a["Type of Vehicle"].isin(selected_a)
    ]

    filtered_b = df_b[
        df_b["Type of Vehicle"].isin(selected_b)
    ]

    # ==========================
    # DYNAMIC KPI CALC
    # ==========================

    def get_vehicle_kpis(df):

        authorized = df["Authorized"].sum()
        held = df["Held"].sum()
        onroad = df["On Road"].sum()
        offroad = df["Off Road"].sum()
        workshop = df["In Workshop"].sum()
        deficiency = df["Deficiency"].sum()

        serviceability = calculate_percentage(
            onroad,
            held
        )

        return {
            "authorized": authorized,
            "held": held,
            "onroad": onroad,
            "offroad": offroad,
            "workshop": workshop,
            "deficiency": deficiency,
            "serviceability": serviceability
        }

    kpi_a = get_vehicle_kpis(filtered_a)
    kpi_b = get_vehicle_kpis(filtered_b)

    # ==========================
    # COMPARISON
    # ==========================

    '''comparison = pd.DataFrame({
        "Category": [
            "Tracked / Armoured",
            "Soft-Skin"
        ],
        "Serviceability": [
            kpi_a["serviceability"],
            kpi_b["serviceability"]
        ],
        "Deficiency": [
            kpi_a["deficiency"],
            kpi_b["deficiency"]
        ]
    })

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            comparison,
            x="Category",
            y="Serviceability",
            title="Serviceability Comparison",
            text_auto=".1f"
        )

        fig.add_hline(y=80)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            comparison,
            x="Category",
            y="Deficiency",
            title="Deficiency Comparison",
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)'''

    # ==========================
    # A VEHICLES
    # ==========================

    st.divider()
    st.subheader(title_a)

    cols = st.columns(6)

    cols[0].metric("Authorized", int(kpi_a["authorized"]))
    cols[1].metric("Held", int(kpi_a["held"]))
    cols[2].metric("On Road", int(kpi_a["onroad"]))
    cols[3].metric("Off Road", int(kpi_a["offroad"]))
    cols[4].metric("Workshop", int(kpi_a["workshop"]))
    cols[5].metric(
        "Serviceability",
        f"{kpi_a['serviceability']:.1f}%"
    )

    st.metric(
        "Deficiency",
        int(kpi_a["deficiency"])
    )

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            px.bar(
                filtered_a,
                x="Type of Vehicle",
                y=["Authorized", "Held"],
                barmode="group",
                title="Authorized vs Held"
            ),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            px.bar(
                filtered_a,
                x="Type of Vehicle",
                y=["On Road", "Off Road", "In Workshop"],
                barmode="stack",
                title="Operational Status"
            ),
            use_container_width=True
        )

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            filtered_a,
            x="Type of Vehicle",
            y="Serviceability %",
            title="Serviceability %",
            text_auto=".1f"
        )

        fig.add_hline(y=80)

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.plotly_chart(
            px.bar(
                filtered_a.sort_values(
                    "Deficiency",
                    ascending=False
                ),
                x="Type of Vehicle",
                y="Deficiency",
                title="Deficiency Analysis",
                text_auto=True
            ),
            use_container_width=True
        )

    '''with st.expander("Detailed Data"):
        st.dataframe(filtered_a, use_container_width=True, hide_index=True)'''
        
    st.subheader("Detailed Data")
    
    st.dataframe(
        filtered_a,
        use_container_width=True,
        hide_index=True
    )

    # ==========================
    # B VEHICLES
    # ==========================

    st.divider()
    st.subheader(title_b)

    cols = st.columns(6)

    cols[0].metric("Authorized", int(kpi_b["authorized"]))
    cols[1].metric("Held", int(kpi_b["held"]))
    cols[2].metric("On Road", int(kpi_b["onroad"]))
    cols[3].metric("Off Road", int(kpi_b["offroad"]))
    cols[4].metric("Workshop", int(kpi_b["workshop"]))
    cols[5].metric(
        "Serviceability",
        f"{kpi_b['serviceability']:.1f}%"
    )

    st.metric(
        "Deficiency",
        int(kpi_b["deficiency"])
    )

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            px.bar(
                filtered_b,
                x="Type of Vehicle",
                y=["Authorized", "Held"],
                barmode="group"
            ),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            px.bar(
                filtered_b,
                x="Type of Vehicle",
                y=["On Road", "Off Road", "In Workshop"],
                barmode="stack"
            ),
            use_container_width=True
        )

    '''left, right = st.columns(2)

    with left:

        fig = px.bar(
            filtered_b,
            x="Type of Vehicle",
            y="Serviceability %",
            text_auto=".1f"
        )

        fig.add_hline(y=80)

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.plotly_chart(
            px.bar(
                filtered_b.sort_values(
                    "Deficiency",
                    ascending=False
                ),
                x="Type of Vehicle",
                y="Deficiency",
                text_auto=True
            ),
            use_container_width=True
        )'''

    '''with st.expander("Detailed Data"):
        st.dataframe(filtered_b, use_container_width=True, hide_index=True)'''
        
    st.subheader("Detailed Data")
    
    st.dataframe(
        filtered_b,
        use_container_width=True,
        hide_index=True
    )