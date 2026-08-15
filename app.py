import streamlit as st
from modules.sheet_02_vehicle import render_vehicle_state
from modules.sheet_03_weapons import render_weapons_state
from modules.sheet_04_critical_equipment import render_critical_equipment
from modules.sheet_05_signals_equipment import render_signals_equipment
from modules.sheet_06_ammunition import render_ammunition_state
from modules.sheet_07_pol import render_pol_state
from modules.sheet_08_audit_objections import render_audit_objections
from modules.sheet_09_training_calendar import render_training_calendar
from modules.sheet_10_promotions import render_promotions
from modules.sheet_11_officers import render_officers

st.set_page_config(
    page_title="Formation Dashboard",
    layout="wide"
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🚛 Vehicle",
    "🔫 Weapons",
    "🔭 Critical Equipment",
    "📡 Signals",
    "💣 Ammunition",
    "⛽ POL",
    "📋 Audit",
    "📅 Calendar",
    "👨‍✈️ Promotions",
    "👔 Officers"
])

with tab1:
    render_vehicle_state()

with tab2:
    render_weapons_state()
    
with tab3:
    render_critical_equipment()
    
with tab4:
    render_signals_equipment()
    
with tab5:
    render_ammunition_state()
    
with tab6:
    render_pol_state()
    
with tab7:
    render_audit_objections()
    
with tab8:
    render_training_calendar()
    
with tab9:
    render_promotions()
    
with tab10:
    render_officers()