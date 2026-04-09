import streamlit as st
import pandas as pd

st.set_page_config(page_title="InBalance Explore", layout="centered")

# -----------------------------
# Load data
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
# Session state
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

def phase_class(phase_name):
    p = phase_name.lower()
    if "menstrual" in p:
        return "menstrual"
    if "follicular" in p:
        return "follicular"
    if "ovulatory" in p or "ovulation" in p:
        return "ovulatory"
    if "luteal" in p:
        return "luteal"
    return "neutral"

def phase_dot_colors(phases_text):
    phases = split_csv_text(phases_text)
    colors = []
    for p in phases:
        cls = phase_class(p)
        if cls == "menstrual":
            colors.append("#d45a7a")
        elif cls == "follicular":
            colors.append("#4fa56f")
        elif cls == "ovulatory":
            colors.append("#d88ac7")
        elif cls == "luteal":
            colors.append("#8e6ad8")
    return colors[:3]

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background: #080606;
    color: #f6efe8;
    font-family: "Georgia", serif;
}

[data-testid="stAppViewContainer"] {
    background: #080606;
}

section.main > div {
    max-width: 560px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

.block-container {
    max-width: 560px;
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
}

h1,h2,h3,h4,p,div,span,label {
    color: #f6efe8;
}

.top-title {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
}

.back-arrow {
    font-size: 1.8rem;
    color: #f1e5d8;
    line-height: 1;
}

.screen-title {
    font-size: 2.15rem;
    font-weight: 600;
    line-height: 1;
    color: #f1e5d8;
}

.segment-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}

.segment-active {
    background: #c48b57;
    color: #1a120f;
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    font-size: 1.15rem;
    font-weight: 600;
}

.segment-inactive {
    background: #221a19;
    color: #8d7d77;
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    font-size: 1.15rem;
    font-weight: 600;
}

div[data-testid="stTextInputRootElement"] input {
    background: #1b1514 !important;
    color: #f1e7dc !important;
    border: 1px solid #2f2523 !important;
    border-radius: 16px !important;
    padding-top: 0.9rem !important;
    padding-bottom: 0.9rem !important;
}

div[data-testid="stTextInputRootElement"] input::placeholder {
    color: #8f7e76 !important;
}

.phase-row {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 4px;
    margin-top: 4px;
    margin-bottom: 18px;
    scrollbar-width: none;
}
.phase-row::-webkit-scrollbar {
    display: none;
}

.phase-chip {
    white-space: nowrap;
    border-radius: 999px;
    padding: 9px 14px;
    font-size: 0.96rem;
    line-height: 1;
    border: 1px solid #312624;
    background: #1c1514;
    color: #f2e7dc;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.phase-chip.active-all {
    background: #c48b57;
    color: #140f0d;
    border-color: #c48b57;
}

.phase-chip.menstrual {
    background: #31141b;
    border-color: #4f232d;
    color: #f3c0ce;
}

.phase-chip.follicular {
    background: #13261b;
    border-color: #244230;
    color: #b8e6c6;
}

.phase-chip.ovulatory {
    background: #301725;
    border-color: #4a253a;
    color: #f2bfdc;
}

.phase-chip.luteal {
    background: #241733;
    border-color: #3a2850;
    color: #d5c2ff;
}

.phase-chip.myphase {
    background: #181818;
    border-color: #2d2d2d;
    color: #f3df8e;
}

.food-card {
    background: #110d0d;
    border: 1px solid #362723;
    border-radius: 20px;
    padding: 16px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.01) inset;
}

.food-card-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.food-emoji {
    font-size: 1.9rem;
    line-height: 1;
}

.food-name {
    font-size: 1.65rem;
    line-height: 1.05;
    font-weight: 500;
    color: #f4ece4;
    margin-bottom: 4px;
}

.food-group {
    font-size: 0.98rem;
    color: #9c8e87;
}

.phase-dots {
    display: flex;
    gap: 5px;
    align-items: center;
}

.phase-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    display: inline-block;
}

div[data-testid="stButton"] button {
    width: 100%;
    background: transparent;
    color: transparent;
    border: none;
    box-shadow: none;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}
div[data-testid="stButton"] button:hover {
    border: none;
    box-shadow: none;
    background: transparent;
}
div[data-testid="stButton"] button p {
    display: none;
}

.back-link {
    color: #c48b57;
    font-size: 1rem;
    margin-bottom: 16px;
}

.detail-card {
    background: #110d0d;
    border: 1px solid #362723;
    border-radius: 24px;
    padding: 24px;
    margin-top: 8px;
}

.detail-emoji {
    font-size: 2.7rem;
    line-height: 1;
}

.detail-title {
    font-size: 2.8rem;
    line-height: 1;
    margin-top: 12px;
    color: #f5ede4;
    font-weight: 500;
}

.detail-group {
    margin-top: 8px;
    color: #9b8d86;
    font-size: 1.05rem;
}

.section-label {
    margin-top: 24px;
    margin-bottom: 8px;
    font-size: 1.35rem;
    font-weight: 600;
    color: #f1e8df;
}

.detail-text {
    color: #d8ccc2;
    font-size: 1.08rem;
    line-height: 1.75;
}

.tag {
    display: inline-block;
    background: #221b1a;
    color: #ece2d7;
    border-radius: 999px;
    padding: 7px 13px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.92rem;
}

.phase-tag {
    display: inline-block;
    border-radius: 999px;
    padding: 7px 13px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.92rem;
    border: 1px solid transparent;
}

.phase-tag.menstrual {
    background: #31141b;
    border-color: #4f232d;
    color: #f3c0ce;
}
.phase-tag.follicular {
    background: #13261b;
    border-color: #244230;
    color: #b8e6c6;
}
.phase-tag.ovulatory {
    background: #301725;
    border-color: #4a253a;
    color: #f2bfdc;
}
.phase-tag.luteal {
    background: #241733;
    border-color: #3a2850;
    color: #d5c2ff;
}
.phase-tag.neutral {
    background: #221b1a;
    border-color: #312624;
    color: #ece2d7;
}

.spacer-small {
    height: 6px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="top-title">
    <div class="back-arrow">←</div>
    <div class="screen-title">Explore</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="segment-wrap">
    <div class="segment-active">🍽️ Food</div>
    <div class="segment-inactive">🏋️ Workouts</div>
</div>
""", unsafe_allow_html=True)

search = st.text_input("", placeholder="Search foods...")

phase_chip_html = f"""
<div class="phase-row">
    <span class="phase-chip {'active-all' if st.session_state.phase_filter == 'All Phases' else ''}">All Phases</span>
    <span class="phase-chip myphase">✨ My Phase</span>
    <span class="phase-chip menstrual">🌙 Menstrual</span>
    <span class="phase-chip follicular">🌱 Follicular</span>
    <span class="phase-chip ovulatory">🌸 Ovulation</span>
    <span class="phase-chip luteal">🔥 Luteal</span>
</div>
"""
st.markdown(phase_chip_html, unsafe_allow_html=True)

phase_options = ["All Phases", "Menstrual", "Follicular", "Ovulatory", "Luteal"]
phase_cols = st.columns(len(phase_options))
for i, phase in enumerate(phase_options):
    with phase_cols[i]:
        if st.button(phase, key=f"phase_{phase}"):
            st.session_state.phase_filter = phase

# -----------------------------
# Filtering
# -----------------------------
filtered = df.copy()

if search:
    filtered = filtered[
        filtered["food_name"].str.contains(search, case=False, na=False)
    ]

if st.session_state.phase_filter != "All Phases":
    filtered = filtered[
        filtered["best_during_phases"].str.contains(st.session_state.phase_filter, case=False, na=False)
    ]

# -----------------------------
# List view
# -----------------------------
if st.session_state.selected_food_id is None:
    for _, row in filtered.iterrows():
        group_name = get_group(row)
        dots = phase_dot_colors(row.get("best_during_phases", ""))
        dots_html = "".join([f"<span class='phase-dot' style='background:{c}'></span>" for c in dots])

        card_html = f"""
        <div class="food-card">
            <div class="food-card-left">
                <div class="food-emoji">{row.get('emoji', '🍽️')}</div>
                <div>
                    <div class="food-name">{row['food_name']}</div>
                    <div class="food-group">{group_name}</div>
                </div>
            </div>
            <div class="phase-dots">{dots_html}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        if st.button(f"open_{row['food_id']}", key=f"open_{row['food_id']}"):
            st.session_state.selected_food_id = row["food_id"]
            st.rerun()

# -----------------------------
# Detail view
# -----------------------------
else:
    selected = df[df["food_id"] == st.session_state.selected_food_id].iloc[0]

    if st.button("back_to_list", key="back_to_list"):
        st.session_state.selected_food_id = None
        st.rerun()

    st.markdown('<div class="back-link">← Back to list</div>', unsafe_allow_html=True)

    st.markdown('<div class="detail-card">', unsafe_allow_html=True)
    st.markdown(f"<div class='detail-emoji'>{selected.get('emoji', '🍽️')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-title'>{selected['food_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-group'>{get_group(selected)}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Benefits</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='detail-text'>{selected.get('description', '')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='section-label'>Key Nutrients</div>", unsafe_allow_html=True)
    nutrient_html = "".join(
        [f"<span class='tag'>{n}</span>" for n in split_csv_text(selected.get("key_nutrients", ""))]
    )
    st.markdown(nutrient_html or "<span class='tag'>No data</span>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Best During</div>", unsafe_allow_html=True)
    phase_html = ""
    for p in split_csv_text(selected.get("best_during_phases", "")):
        phase_html += f"<span class='phase-tag {phase_class(p)}'>{p}</span>"
    st.markdown(phase_html or "<span class='tag'>No data</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
