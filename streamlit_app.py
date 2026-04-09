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

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #000000;
    color: #f5e9dc;
    font-family: Georgia, serif;
}

.block-container {
    max-width: 760px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.title-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1rem;
}

.explore-title {
    font-size: 2.2rem;
    font-weight: 600;
    margin: 0;
}

.toggle-wrap {
    display: flex;
    gap: 10px;
    margin-bottom: 1rem;
}

.toggle-active {
    flex: 1;
    text-align: center;
    background: #d6a063;
    color: black;
    padding: 14px 18px;
    border-radius: 18px;
    font-weight: 600;
}

.toggle-inactive {
    flex: 1;
    text-align: center;
    background: #231d1b;
    color: #8a7e75;
    padding: 14px 18px;
    border-radius: 18px;
    font-weight: 600;
}

.food-card {
    background: #120f0e;
    border: 1px solid #3b2d23;
    border-radius: 22px;
    padding: 16px 18px;
    margin-bottom: 12px;
}

.food-name {
    font-size: 1.35rem;
    font-weight: 600;
    color: #f7ede4;
}

.food-group {
    font-size: 0.95rem;
    color: #9e9388;
}

.detail-card {
    background: #120f0e;
    border: 1px solid #3b2d23;
    border-radius: 28px;
    padding: 28px;
    margin-top: 18px;
}

.detail-title {
    font-size: 2.2rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
}

.detail-sub {
    color: #9e9388;
    margin-bottom: 1.2rem;
}

.label {
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}

.pill {
    display: inline-block;
    background: #24201e;
    color: #f3e7dc;
    border-radius: 999px;
    padding: 8px 14px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.phase-pill {
    display: inline-block;
    border-radius: 999px;
    padding: 8px 14px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.9rem;
    border: 1px solid transparent;
}

.menstrual { background: rgba(127, 29, 29, 0.35); color: #fda4af; border-color: rgba(251, 113, 133, 0.25); }
.follicular { background: rgba(20, 83, 45, 0.35); color: #86efac; border-color: rgba(134, 239, 172, 0.25); }
.ovulatory { background: rgba(131, 24, 67, 0.35); color: #f9a8d4; border-color: rgba(249, 168, 212, 0.25); }
.luteal { background: rgba(76, 29, 149, 0.35); color: #c4b5fd; border-color: rgba(196, 181, 253, 0.25); }

.stTextInput > div > div > input {
    background-color: #231d1b;
    color: #f5e9dc;
    border-radius: 16px;
}

div[data-testid="stButton"] button {
    width: 100%;
    border-radius: 16px;
    background: #120f0e;
    color: #f5e9dc;
    border: 1px solid #3b2d23;
    padding: 0.8rem 1rem;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

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
    return ""

st.markdown("""
<div class="title-row">
    <div style="font-size: 2rem;">←</div>
    <div class="explore-title">Explore</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="toggle-wrap">
    <div class="toggle-active">🍽️ Food</div>
    <div class="toggle-inactive">🏋️ Workouts</div>
</div>
""", unsafe_allow_html=True)

search = st.text_input("", placeholder="Search foods...")

phase_options = ["All Phases", "Menstrual", "Follicular", "Ovulatory", "Luteal"]
phase_cols = st.columns(len(phase_options))

for i, phase in enumerate(phase_options):
    with phase_cols[i]:
        if st.button(phase, key=f"phase_{phase}"):
            st.session_state.phase_filter = phase

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["food_name"].str.contains(search, case=False, na=False)
    ]

if st.session_state.phase_filter != "All Phases":
    filtered = filtered[
        filtered["best_during_phases"].str.contains(st.session_state.phase_filter, case=False, na=False)
    ]

if st.session_state.selected_food_id is None:
    for _, row in filtered.iterrows():
        food_label = f"{row.get('emoji', '🍽️')}  {row['food_name']}"
        sub = get_group(row)

        st.markdown(
            f'''
            <div class="food-card">
                <div class="food-name">{food_label}</div>
                <div class="food-group">{sub}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        if st.button(f"Open {row['food_name']}", key=f"open_{row['food_id']}"):
            st.session_state.selected_food_id = row["food_id"]
            st.rerun()
else:
    selected = df[df["food_id"] == st.session_state.selected_food_id].iloc[0]

    if st.button("← Back to list"):
        st.session_state.selected_food_id = None
        st.rerun()

    st.markdown('<div class="detail-card">', unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:3rem'>{selected.get('emoji', '🍽️')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-title'>{selected['food_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-sub'>{get_group(selected)}</div>", unsafe_allow_html=True)

    st.markdown("<div class='label'>Benefits</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:1.05rem; line-height:1.8; color:#dbcfc4'>{selected.get('description','')}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='label'>Key Nutrients</div>", unsafe_allow_html=True)
    nutrient_html = "".join(
        [f"<span class='pill'>{n}</span>" for n in split_csv_text(selected.get("key_nutrients", ""))]
    )
    st.markdown(nutrient_html or "<span class='pill'>No data</span>", unsafe_allow_html=True)

    st.markdown("<div class='label'>Best During</div>", unsafe_allow_html=True)
    phase_html = ""
    for p in split_csv_text(selected.get("best_during_phases", "")):
        phase_html += f"<span class='phase-pill {phase_class(p)}'>{p}</span>"
    st.markdown(phase_html or "<span class='pill'>No data</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
