import streamlit as st
import pandas as pd

st.set_page_config(page_title="InBalance Explore", layout="centered")

# =============================
# COLOR SETTINGS — change these
# =============================
BG = "#070505"
CARD = "#120d0c"
CARD_BORDER = "#3a2824"
TEXT = "#f4ebe2"
MUTED = "#a39289"
ACCENT = "#c77f4f"
TAB_OFF = "#211918"
SEARCH_BG = "#1a1413"

PHASE_COLORS = {
    "menstrual": {"bg": "#34131d", "text": "#f3bfd0", "border": "#4e2230", "dot": "#df6b8b"},
    "follicular": {"bg": "#13261b", "text": "#bfe7ca", "border": "#254232", "dot": "#63b77c"},
    "ovulatory": {"bg": "#301725", "text": "#f0c0dc", "border": "#492538", "dot": "#d989c5"},
    "luteal": {"bg": "#251736", "text": "#d7c3ff", "border": "#3b2951", "dot": "#9677e7"},
    "neutral": {"bg": "#221a19", "text": "#ece0d4", "border": "#332623", "dot": "#b8a59a"},
}

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    df = pd.read_csv("explore_foods.csv")
    for col in ["food_name", "description", "key_nutrients", "best_during_phases", "emoji"]:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df

df = load_data()

# =============================
# SESSION STATE
# =============================
if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = None

if "phase_filter" not in st.session_state:
    st.session_state.phase_filter = "All Phases"

# =============================
# HELPERS
# =============================
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
    return [PHASE_COLORS[phase_class(p)]["dot"] for p in phases[:3]]

# =============================
# CSS
# =============================
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
    max-width: 560px;
    padding-top: 1.1rem !important;
    padding-bottom: 3rem !important;
}}

h1,h2,h3,h4,p,div,span,label {{
    color: {TEXT};
}}

.top-title {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
}}

.back-arrow {{
    font-size: 1.7rem;
    line-height: 1;
}}

.screen-title {{
    font-size: 2.2rem;
    font-weight: 600;
    line-height: 1;
}}

.segment-wrap {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}}

.segment-active {{
    background: {ACCENT};
    color: #1b110d;
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    font-size: 1.08rem;
    font-weight: 600;
}}

.segment-inactive {{
    background: {TAB_OFF};
    color: #8d7c75;
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    font-size: 1.08rem;
    font-weight: 600;
}}

div[data-testid="stTextInputRootElement"] input {{
    background: {SEARCH_BG} !important;
    color: {TEXT} !important;
    border: 1px solid #2f2320 !important;
    border-radius: 16px !important;
}}

div[data-testid="stTextInputRootElement"] input::placeholder {{
    color: #8e7e77 !important;
}}

.phase-visual-row {{
    display: flex;
    gap: 8px;
    overflow-x: auto;
    margin-top: 6px;
    margin-bottom: 12px;
    padding-bottom: 4px;
    scrollbar-width: none;
}}
.phase-visual-row::-webkit-scrollbar {{
    display: none;
}}

.phase-chip {{
    white-space: nowrap;
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 0.94rem;
    border: 1px solid #332623;
    background: #1a1413;
    color: {TEXT};
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}

.phase-chip.all {{
    background: {ACCENT};
    color: #1b110d;
    border-color: {ACCENT};
}}

.phase-chip.myphase {{
    background: #171717;
    color: #f2de84;
    border-color: #292929;
}}

.phase-filter-buttons {{
    margin-bottom: 14px;
}}

div[data-testid="stHorizontalBlock"] > div {{
    padding-left: 0.12rem !important;
    padding-right: 0.12rem !important;
}}

div[data-testid="stButton"] > button {{
    width: 100%;
    border-radius: 999px;
    background: #1a1413;
    color: {TEXT};
    border: 1px solid #332623;
    padding: 0.45rem 0.5rem;
    font-size: 0.78rem;
}}

div[data-testid="stButton"] > button:hover {{
    border-color: {ACCENT};
    color: {TEXT};
}}

.food-shell {{
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-radius: 20px;
    padding: 14px 16px;
    margin-bottom: 8px;
}}

.food-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.food-left {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.food-emoji {{
    font-size: 1.9rem;
    line-height: 1;
}}

.food-name {{
    font-size: 1.55rem;
    line-height: 1.05;
    font-weight: 500;
    margin-bottom: 4px;
}}

.food-group {{
    font-size: 0.95rem;
    color: {MUTED};
}}

.dot-row {{
    display: flex;
    gap: 6px;
    align-items: center;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 999px;
    display: inline-block;
}}

.open-row {{
    margin-top: 10px;
}}

.open-row div[data-testid="stButton"] > button {{
    border-radius: 14px !important;
    background: #181110 !important;
    border: 1px solid #2d201d !important;
    color: #eadfd4 !important;
    font-size: 0.93rem !important;
    padding: 0.55rem 0.8rem !important;
}}

.back-link {{
    color: {ACCENT};
    margin: 4px 0 12px 0;
    font-size: 1rem;
}}

.detail-card {{
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-radius: 24px;
    padding: 24px;
    margin-top: 4px;
}}

.detail-emoji {{
    font-size: 2.6rem;
    line-height: 1;
}}

.detail-title {{
    font-size: 2.7rem;
    line-height: 1;
    margin-top: 12px;
    font-weight: 500;
}}

.detail-group {{
    margin-top: 8px;
    color: {MUTED};
    font-size: 1.02rem;
}}

.section-label {{
    margin-top: 24px;
    margin-bottom: 8px;
    font-size: 1.24rem;
    font-weight: 600;
}}

.detail-text {{
    color: #d8ccc1;
    font-size: 1.05rem;
    line-height: 1.75;
}}

.tag {{
    display: inline-block;
    background: #221a18;
    color: #ece1d5;
    border-radius: 999px;
    padding: 7px 13px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.92rem;
}}

.phase-tag {{
    display: inline-block;
    border-radius: 999px;
    padding: 7px 13px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.92rem;
    border: 1px solid transparent;
}}
</style>
""", unsafe_allow_html=True)

# dynamic phase tag classes
extra_css = ""
for key, vals in PHASE_COLORS.items():
    extra_css += f"""
    .phase-tag.{key} {{
        background: {vals['bg']};
        color: {vals['text']};
        border-color: {vals['border']};
    }}
    .phase-chip-{key} {{
        background: {vals['bg']};
        color: {vals['text']};
        border: 1px solid {vals['border']};
    }}
    """
st.markdown(f"<style>{extra_css}</style>", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown("""
<div class="top-title">
    <div class="back-arrow">←</div>
    <div class="screen-title">Explore</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="segment-wrap">
    <div class="segment-active">🍽 Food</div>
    <div class="segment-inactive">🏋 Workouts</div>
</div>
""", unsafe_allow_html=True)

search = st.text_input("", placeholder="Search foods...")

active_all = "all" if st.session_state.phase_filter == "All Phases" else ""
st.markdown(f"""
<div class="phase-visual-row">
    <span class="phase-chip {active_all}">All Phases</span>
    <span class="phase-chip myphase">✨ My Phase</span>
    <span class="phase-chip phase-chip-menstrual">🌙 Menstrual</span>
    <span class="phase-chip phase-chip-follicular">🌱 Follicular</span>
    <span class="phase-chip phase-chip-ovulatory">🌸 Ovulation</span>
    <span class="phase-chip phase-chip-luteal">🔥 Luteal</span>
</div>
""", unsafe_allow_html=True)

phase_options = ["All Phases", "Menstrual", "Follicular", "Ovulatory", "Luteal"]
cols = st.columns(len(phase_options))
for i, phase in enumerate(phase_options):
    with cols[i]:
        if st.button(phase, key=f"phase_{phase}"):
            st.session_state.phase_filter = phase

# =============================
# FILTER
# =============================
filtered = df.copy()

if search:
    filtered = filtered[filtered["food_name"].str.contains(search, case=False, na=False)]

if st.session_state.phase_filter != "All Phases":
    filtered = filtered[
        filtered["best_during_phases"].str.contains(st.session_state.phase_filter, case=False, na=False)
    ]

# =============================
# LIST VIEW
# =============================
if st.session_state.selected_food_id is None:
    for _, row in filtered.iterrows():
        dots_html = "".join(
            [f"<span class='dot' style='background:{c}'></span>" for c in phase_dots(row.get("best_during_phases", ""))]
        )

        st.markdown(f"""
        <div class="food-shell">
            <div class="food-row">
                <div class="food-left">
                    <div class="food-emoji">{row.get('emoji', '🍽️')}</div>
                    <div>
                        <div class="food-name">{row['food_name']}</div>
                        <div class="food-group">{get_group(row)}</div>
                    </div>
                </div>
                <div class="dot-row">{dots_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(f"Open {row['food_name']}", key=f"open_{row['food_id']}"):
                st.session_state.selected_food_id = row["food_id"]
                st.rerun()
        with col2:
            st.write("")

# =============================
# DETAIL VIEW
# =============================
else:
    selected = df[df["food_id"] == st.session_state.selected_food_id].iloc[0]

    if st.button("← Back to list", key="back_to_list"):
        st.session_state.selected_food_id = None
        st.rerun()

    st.markdown('<div class="detail-card">', unsafe_allow_html=True)
    st.markdown(f"<div class='detail-emoji'>{selected.get('emoji', '🍽️')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-title'>{selected['food_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-group'>{get_group(selected)}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Benefits</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-text'>{selected.get('description', '')}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Key Nutrients</div>", unsafe_allow_html=True)
    nutrient_html = "".join(
        [f"<span class='tag'>{n}</span>" for n in split_csv_text(selected.get("key_nutrients", ""))]
    )
    st.markdown(nutrient_html or "<span class='tag'>No data</span>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Best During</div>", unsafe_allow_html=True)
    phase_html = "".join(
        [f"<span class='phase-tag {phase_class(p)}'>{p}</span>" for p in split_csv_text(selected.get("best_during_phases", ""))]
    )
    st.markdown(phase_html or "<span class='tag'>No data</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
