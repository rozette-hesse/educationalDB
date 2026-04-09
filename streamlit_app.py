import streamlit as st
import pandas as pd

st.set_page_config(page_title="InBalance Explore", layout="centered")

# -----------------------------
# Theme
# -----------------------------
BG = "#f3dddd"        # page background
CARD = "#2a1f24"      # main cards
BORDER = "#4a3940"    # borders
TEXT = "#fff7f8"      # main text
MUTED = "#cbb7bd"     # muted text
ACCENT = "#b88aa0"    # active tab
ACCENT_2 = "#97b29f"  # optional sage accent

PHASE_STYLES = {
    "menstrual": {"bg": "#b86f87", "text": "#fff6f8"},
    "follicular": {"bg": "#8daa96", "text": "#fbfffc"},
    "ovulatory": {"bg": "#c792b3", "text": "#fff8fc"},
    "luteal": {"bg": "#9a88bb", "text": "#fcfaff"},
    "neutral": {"bg": "#dbc8cf", "text": "#5a4650"},
}

# -----------------------------
# Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("explore_foods.csv")
    for col in ["food_name", "description", "key_nutrients", "best_during_phases", "emoji"]:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df

df = load_data()

# -----------------------------
# Session
# -----------------------------
if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = None

if "phase_filter" not in st.session_state:
    st.session_state.phase_filter = "All Phases"

# -----------------------------
# Helpers
# -----------------------------
def split_csv_text(text):
    if not text:
        return []
    return [x.strip() for x in str(text).split(",") if x.strip()]

def get_group(row):
    for col in ["food_group", "main_group", "food_subgroup", "subgroup"]:
        if col in row and pd.notna(row[col]) and str(row[col]).strip():
            return str(row[col]).replace("_", " ").title()
    return "Food"

def phase_class(name):
    x = str(name).lower()
    if "menstrual" in x:
        return "menstrual"
    if "follicular" in x:
        return "follicular"
    if "ovulatory" in x or "ovulation" in x:
        return "ovulatory"
    if "luteal" in x:
        return "luteal"
    return "neutral"

def phase_dots(text):
    phases = split_csv_text(text)
    colors = []
    for p in phases[:3]:
        c = phase_class(p)
        if c == "menstrual":
            colors.append("#d97d98")
        elif c == "follicular":
            colors.append("#93b8a1")
        elif c == "ovulatory":
            colors.append("#d3a0bf")
        elif c == "luteal":
            colors.append("#ab97cb")
    return colors

def render_phase_tag(label):
    cls = phase_class(label)
    style = PHASE_STYLES.get(cls, PHASE_STYLES["neutral"])
    st.markdown(
        f"""
        <span style="
            display:inline-block;
            padding:7px 13px;
            margin:0 8px 8px 0;
            border-radius:999px;
            background:{style['bg']};
            color:{style['text']};
            font-size:0.92rem;
        ">{label}</span>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# CSS
# -----------------------------
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    background: {BG};
    color: {TEXT};
    font-family: Georgia, serif;
}}

[data-testid="stAppViewContainer"] {{
    background: {BG};
}}

.block-container {{
    max-width: 620px;
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
}}

h1, h2, h3, h4, h5, p, div, span, label {{
    color: {TEXT};
}}

div[data-testid="stTextInputRootElement"] input {{
    background: #f8eef1 !important;
    color: #533f48 !important;
    border: 1px solid #d8c2ca !important;
    border-radius: 18px !important;
}}

div[data-testid="stTextInputRootElement"] input::placeholder {{
    color: #9e8790 !important;
}}

div[data-testid="stButton"] > button {{
    border-radius: 16px;
    background: #e6d6db !important;
    color: #4d3942 !important;
    border: 1px solid #d4bec6 !important;
    box-shadow: none !important;
}}

div[data-testid="stButton"] > button:hover {{
    background: #dcc8cf !important;
    color: #4d3942 !important;
    border: 1px solid #cdb1bb !important;
}}

.explore-title {{
    font-size: 2.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #4d3942;
}}

.segment-wrap {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 1rem;
}}

.segment-on {{
    background: #c39ab0;
    color: #2f2027;
    border-radius: 18px;
    padding: 14px 16px;
    text-align: center;
    font-size: 1.08rem;
    font-weight: 600;
}}

.segment-off {{
    background: #3a2b31;
    color: #d8c7ce;
    border-radius: 18px;
    padding: 14px 16px;
    text-align: center;
    font-size: 1.08rem;
    font-weight: 600;
}}

.card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 14px 16px;
    margin-bottom: 10px;
}}

.card-name {{
    font-size: 1.45rem;
    font-weight: 600;
    line-height: 1.1;
}}

.card-group {{
    color: {MUTED};
    font-size: 0.96rem;
    margin-top: 4px;
}}

.detail-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 26px;
    padding: 24px;
    margin-top: 10px;
}}

.label {{
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}}

.tag {{
    display: inline-block;
    background: #e6d4db;
    color: #523f48;
    padding: 7px 13px;
    border-radius: 999px;
    margin: 0 8px 8px 0;
    font-size: 0.92rem;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="explore-title">← Explore</div>', unsafe_allow_html=True)

st.markdown("""
<div class="segment-wrap">
    <div class="segment-on">Food</div>
    <div class="segment-off">Workouts</div>
</div>
""", unsafe_allow_html=True)

search = st.text_input("", placeholder="Search foods...")

# -----------------------------
# Phase filters
# -----------------------------
phase_options = ["All Phases", "Menstrual", "Follicular", "Ovulatory", "Luteal"]
phase_cols = st.columns(len(phase_options))

for i, phase in enumerate(phase_options):
    with phase_cols[i]:
        button_type = "primary" if st.session_state.phase_filter == phase else "secondary"
        if st.button(phase, key=f"phase_{phase}", use_container_width=True, type=button_type):
            st.session_state.phase_filter = phase

# -----------------------------
# Filter data
# -----------------------------
filtered = df.copy()

if search:
    filtered = filtered[filtered["food_name"].str.contains(search, case=False, na=False)]

if st.session_state.phase_filter != "All Phases":
    filtered = filtered[
        filtered["best_during_phases"].str.contains(st.session_state.phase_filter, case=False, na=False)
    ]

# -----------------------------
# List view
# -----------------------------
if st.session_state.selected_food_id is None:
    for _, row in filtered.iterrows():
        dots = phase_dots(row.get("best_during_phases", ""))
        dots_html = "".join([
            f"<span style='display:inline-block;width:10px;height:10px;border-radius:999px;background:{c};margin-left:6px;'></span>"
            for c in dots
        ])

        st.markdown(
            f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
                    <div style="display:flex;align-items:center;gap:12px;">
                        <div style="font-size:1.9rem;">{row.get('emoji','🍽️')}</div>
                        <div>
                            <div class="card-name">{row['food_name']}</div>
                            <div class="card-group">{get_group(row)}</div>
                        </div>
                    </div>
                    <div>{dots_html}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(f"Open {row['food_name']}", key=f"open_{row['food_id']}", use_container_width=True):
            st.session_state.selected_food_id = row["food_id"]
            st.rerun()

# -----------------------------
# Detail view
# -----------------------------
else:
    selected = df[df["food_id"] == st.session_state.selected_food_id].iloc[0]

    if st.button("← Back to list", key="back_to_list"):
        st.session_state.selected_food_id = None
        st.rerun()

    st.markdown('<div class="detail-card">', unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:2.8rem'>{selected.get('emoji','🍽️')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:2.4rem;font-weight:600;margin-top:10px'>{selected['food_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:{MUTED};margin-top:6px'>{get_group(selected)}</div>", unsafe_allow_html=True)

    st.markdown('<div class="label">Benefits</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div style='color:#f0e4e8;line-height:1.75;font-size:1.03rem'>{selected.get('description','')}</div>",
        unsafe_allow_html=True
    )

    st.markdown('<div class="label">Key Nutrients</div>', unsafe_allow_html=True)
    nutrients = split_csv_text(selected.get("key_nutrients", ""))
    if nutrients:
        for n in nutrients:
            st.markdown(f"<span class='tag'>{n}</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='tag'>No data</span>", unsafe_allow_html=True)

    st.markdown('<div class="label">Best During</div>', unsafe_allow_html=True)
    phases = split_csv_text(selected.get("best_during_phases", ""))
    if phases:
        for p in phases:
            render_phase_tag(p)
    else:
        st.markdown("<span class='tag'>No data</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
