import streamlit as st

# --- Kennzahlen aus Notebook 02 (hardcoded, kein Shapefile-Laden) ---
HOTSPOTS = {"Sundarbans": {
    "area_1996_km2": 6313.3,
    "area_2020_km2": 6293.2,
    "loss_km2": 20.1,
    "carbon_loss_t": 2006150,
    "market_value": 60184505,
}}

# --- Seitenbreite auf "wide" setzen, Titel anzeigen ---
st.set_page_config(page_title="Mangroven-Loss-Tracker", layout="wide")
st.title("Mangroven-Loss-Tracker")

# --- Sidebar: Dropdown für Hotspot-Auswahl ---
with st.sidebar:
    st.header("Hotspot")
    hotspot = st.selectbox("Region wählen", list(HOTSPOTS.keys()))

# --- Aktiven Hotspot aus Dictionary laden ---
data = HOTSPOTS[hotspot]

# --- 3 Spalten: Fläche 1996 / Fläche 2020 / Verlust ---
col1, col2, col3 = st.columns(3)
col1.metric("Fläche 1996", f"{data['area_1996_km2']:,.0f} km²")
col2.metric("Fläche 2020", f"{data['area_2020_km2']:,.0f} km²")
col3.metric("Verlust", f"{data['loss_km2']:,.1f} km²", delta=f"-{data['loss_km2']:,.1f} km²", delta_color="inverse")

# --- Carbon-Kennzahlen darunter ---
st.divider()
st.subheader("Carbon Impact")
st.metric("Carbon-Verlust", f"{data['carbon_loss_t']:,.0f} t CO₂e")
st.metric("Marktwert", f"${data['market_value']:,.0f}")

# --- Karte einbinden (vorberechnetes leafmap HTML) ---
st.divider()
st.subheader("Karte")

st.image("assets/precomputed/sundarbans_matplotlib.png", use_container_width=True)
