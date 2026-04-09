import streamlit as st
import pandas as pd

st.set_page_config(page_title="InBalance Explore", layout="centered")

@st.cache_data
def load_data():
    df = pd.read_csv("explore_foods.csv")
    for col in ["food_name", "description", "key_nutrients", "best_during_phases", "emoji"]:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df

df = load_data()

if "selected_food_id" not in st.session_state:
    st.session_state.selected_food_id = None

if "phase_filter" not in st.session_state:
    st.session_state.phase_filter = "All Phases"


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
            colors.append("#E06C8A")
        elif cls == "follicular":
            colors.append("#69B77C")
        elif cls == "ovulatory":
            colors.append("#D88BC8")
        elif cls == "luteal":
            colors.append("#9B7BEA")
    return colors[:3]


st.markdown("""
<style>
html, body, [class*="css"] {
    background: #090606;
    color: #F6EEE8;
    font-family: Georgia, serif;
}

[data-testid="stAppViewContainer"] {
    background: #090606;
}

.block-container {
    max-width: 560px;
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
}

h1,h2,h3,h4,p,div,span,label {
    color: #F6EEE8;
}

.top-title {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
}

.back-arrow {
    font-size: 1.8rem;
    color: #F2E7DB;
    line-height: 1;
}

.screen-title {
    font-size: 2.2rem;
    font-weight: 600;
    line-height: 1;
    color: #F2E7DB;
}

.segment-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}

.segment-active {
    background: #C98A56;
    color: #1B120E;
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    font-size: 1.08rem;
    font-weight: 600;
}

.segment-inactive {
    background: #211918;
    color: #8E7F79;
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    font-size: 1.08rem;
    font-weight: 600;
}

div[data-testid="stTextInputRootElement"] input {
    background: #1A1413 !important;
    color: #F2E7DB !important;
    border: 1px solid #312422 !important;
    border-radius: 16px !important;
}

div[data-testid="stTextInputRootElement"] input::placeholder {
    color: #8E7F79 !important;
}

.phase-scroll {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    margin-top: 6px;
    margin-bottom: 14px;
    padding-bottom: 4px;
    scrollbar-width: none;
}
.phase-scroll::-webkit-scrollbar {
    display: none;
}

.phase-chip {
    white-space: nowrap;
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 0.95rem;
    border: 1px solid #332522;
    background: #1A1413;
    color: #F2E7DB;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.phase-chip.active-all {
    background: #C98A56;
    color: #1B120E;
    border-color: #C98A56;
}

.phase-chip.myphase {
    background: #171717;
    color: #F2DE84;
    border-color: #2A2A2A;
}

.phase-chip.menstrual {
    background: #31131B;
    color: #F3BECD;
    border-color: #4B212C;
}

.phase-chip.follicular {
    background: #12241A;
    color: #BCE5C7;
    border-color: #234031;
}

.phase-chip.ovulatory {
    background: #2E1624;
    color: #F2C1DD;
    border-color: #472338;
}

.phase-chip.luteal {
    background: #241634;
    color: #D7C4FF;
    border-color: #3A2850;
}

.phase-filter-row {
    margin-top: -2px;
    margin-bottom: 14px;
}

div[data-testid="stHorizontalBlock"] > div:has(button[kind]) {
    flex: 1 1 0%;
}

div[data-testid="stButton"] > button {
    width: 100%;
    border-radius: 999px;
    background: #1A1413;
    color: #F2E7DB;
    border: 1px solid #332522;
    padding: 0.45rem 0.6rem;
    font-size: 0.78rem;
}

div[data-testid="stButton"] > button:hover {
    border-color: #C98A56;
    color: #F2E7DB;
}

.card-button button {
    text-align: left !important;
    background: #110D0D !important;
    border: 1px solid #372723 !important;
    border-radius: 20px !important;
    padding: 0 !important;
    overflow: hidden;
}

.card-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 18px;
}

.card-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.card-emoji {
    font-size: 2rem;
    line-height: 1;
}

.card-name {
    font-size: 1.6rem;
    line-height: 1.05;
    font-weight: 500;
    color: #F4ECE5;
    margin-bottom: 4px;
}

.card-group {
    font-size: 0.96rem;
    color: #9C8E88;
}

.card-dots {
    display: flex;
    gap: 6px;
    align-items: center;
}

.card-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    display: inline-block;
}

.back-link {
    color: #C98A56;
    font-size: 1rem;
    margin: 6px 0 14px 0;
}

.detail-card {
    background: #110D0D;
    border: 1px solid #372723;
    border-radius: 24px;
    padding: 24px;
    margin-top: 4px;
}

.detail-emoji {
    font-size: 2.8rem;
    line-height: 1;
}

.detail-title {
    font-size: 2.7rem;
    line-height: 1;
    margin-top: 12px;
    color: #F4ECE5;
    font-weight: 500;
}

.detail-group {
    margin-top: 8px;
    color: #9C8E88;
    font-size: 1.02rem;
}

.section-label {
    margin-top: 24px;
    margin-bottom: 8px;
    font-size: 1.28rem;
    font-weight: 600;
    color: #F2E8DE;
}

.detail-text {
    color: #DACEC3;
    font-size: 1.06rem;
    line-height: 1.75;
}

.tag {
    display: inline-block;
    background: #221B1A;
    color: #ECE2D8;
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
    background: #31131B;
    color: #F3BECD;
    border-color: #4B212C;
}
.phase-tag.follicular {
    background: #12241A;
    color: #BCE5C7;
    border-color: #234031;
}
.phase-tag.ovulatory {
    background: #2E1624;
    color: #F2C1DD;
    border-color: #472338;
}
.phase-tag.luteal {
    background: #241634;
    color: #D7C4FF;
    border-color: #3A2850;
}
.phase-tag.neutral {
    background: #221B1A;
    color: #ECE2D8;
    border-color: #332522;
}
</style>
""", unsafe_allow_html=True)

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

st.markdown(f"""
<div class="phase-scroll">
    <span class="phase-chip {'active-all' if st.session_state.phase_filter == 'All Phases' else ''}">All Phases</span>
    <span class="phase-chip myphase">✨ My Phase</span>
    <span class="phase-chip menstrual">🌙 Menstrual</span>
    <span class="phase-chip follicular">🌱 Follicular</span>
    <span class="phase-chip ovulatory">🌸 Ovulation</span>
    <span class="phase-chip luteal">🔥 Luteal</span>
</div>
""", unsafe_allow_html=True)

phase_options = ["All Phases", "Menstrual", "Follicular", "Ovulatory", "Luteal"]
with st.container():
    cols = st.columns(len(phase_options))
    for i, phase in enumerate(phase_options):
        with cols[i]:
            if st.button(phase, key=f"phase_{phase}"):
                st.session_state.phase_filter = phase

filtered = df.copy()

if search:
    filtered = filtered[filtered["food_name"].str.contains(search, case=False, na=False)]

if st.session_state.phase_filter != "All Phases":
    filtered = filtered[
        filtered["best_during_phases"].str.contains(st.session_state.phase_filter, case=False, na=False)
    ]

if st.session_state.selected_food_id is None:
    for _, row in filtered.iterrows():
        group_name = get_group(row)
        dots = phase_dot_colors(row.get("best_during_phases", ""))
        dots_html = "".join([f"<span class='card-dot' style='background:{c}'></span>" for c in dots])

        button_label = f"""
        <div class="card-inner">
            <div class="card-left">
                <div class="card-emoji">{row.get('emoji', '🍽️')}</div>
                <div>
                    <div class="card-name">{row['food_name']}</div>
                    <div class="card-group">{group_name}</div>
                </div>
            </div>
            <div class="card-dots">{dots_html}</div>
        </div>
        """

        st.markdown('<div class="card-button">', unsafe_allow_html=True)
        if st.button(button_label, key=f"food_{row['food_id']}"):
            st.session_state.selected_food_id = row["food_id"]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
