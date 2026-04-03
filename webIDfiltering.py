import streamlit as st
import json
import os
from pathlib import Path

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Skin Filter",
    page_icon="🔪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Custom CSS
# -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

.stApp {
    background-color: #0d0f14;
    color: #c8cdd8;
}

/* Header */
.main-title {
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #e2e8f0;
    border-bottom: 2px solid #2a7fff;
    padding-bottom: 0.4rem;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 0.95rem;
    color: #556;
    letter-spacing: 0.08em;
    margin-bottom: 1.5rem;
    font-family: 'Share Tech Mono', monospace;
}

/* Item cards */
.item-card {
    background: #13161e;
    border: 1px solid #1e2330;
    border-left: 3px solid #2a7fff;
    border-radius: 4px;
    padding: 0.55rem 1rem;
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.15s, background 0.15s;
}

.item-card:hover {
    border-left-color: #60abff;
    background: #161926;
}

.item-id {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #2a7fff;
    background: #0a1428;
    border: 1px solid #1a3a70;
    border-radius: 3px;
    padding: 0.15rem 0.5rem;
    min-width: 3.5rem;
    text-align: center;
    letter-spacing: 0.05em;
}

.item-name {
    font-size: 1.05rem;
    font-weight: 600;
    color: #d0d8e8;
    letter-spacing: 0.03em;
}

.item-weapon {
    color: #7a8aaa;
    font-weight: 500;
}

.item-skin {
    color: #e2e8f0;
}

.separator {
    color: #2a7fff;
    margin: 0 0.3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1218;
    border-right: 1px solid #1e2330;
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #2a7fff;
    font-family: 'Rajdhani', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.85rem;
}

/* Stats badge */
.stats-bar {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}

.stat-badge {
    background: #13161e;
    border: 1px solid #1e2330;
    border-radius: 4px;
    padding: 0.3rem 0.75rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: #7a8aaa;
}

.stat-badge span {
    color: #2a7fff;
    font-weight: 700;
}

/* Quality box */
.quality-block {
    background: #13161e;
    border: 1px solid #1e2330;
    border-radius: 4px;
    padding: 0.8rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    line-height: 2;
    color: #7a9aaa;
    margin-bottom: 1rem;
}

.quality-block .q-title {
    color: #2a7fff;
    font-weight: 700;
    font-size: 0.82rem;
    display: block;
    margin-bottom: 0.3rem;
    letter-spacing: 0.1em;
}

.q-fn  { color: #4caf50; }
.q-mw  { color: #8bc34a; }
.q-ft  { color: #ffc107; }
.q-ww  { color: #ff9800; }
.q-bs  { color: #f44336; }

/* Input overrides */
.stTextInput > div > div > input {
    background-color: #13161e !important;
    border: 1px solid #1e2330 !important;
    border-radius: 4px !important;
    color: #e2e8f0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.95rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #2a7fff !important;
    box-shadow: 0 0 0 2px rgba(42,127,255,0.15) !important;
}

.stSelectbox > div > div {
    background-color: #13161e !important;
    border: 1px solid #1e2330 !important;
    color: #e2e8f0 !important;
}

.stTextArea textarea {
    background-color: #0a0d12 !important;
    border: 1px solid #1e2330 !important;
    color: #2a7fff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* No results */
.no-results {
    text-align: center;
    padding: 3rem;
    color: #334;
    font-size: 1.1rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace;
}

/* Error box */
.error-box {
    background: #1a0a0a;
    border: 1px solid #5a1a1a;
    border-left: 3px solid #f44336;
    border-radius: 4px;
    padding: 1rem;
    color: #f44336;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
}

/* Divider line */
hr {
    border: none;
    border-top: 1px solid #1e2330;
    margin: 1rem 0;
}

/* Multiselect */
.stMultiSelect > div {
    background-color: #13161e !important;
    border: 1px solid #1e2330 !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -----------------------
# Load JSON Data
# -----------------------
@st.cache_data
def load_items(filepath="gitskins.json"):
    """Load items from gitskins.json.
    Supports both formats:
      - List:  [{"ID": "Qt", "skin": "AWP | Acheron"}, ...]
      - Dict:  {"Qt": "AWP | Acheron", ...}
    """
    if not Path(filepath).exists():
        return None, f"File not found: `{filepath}` — make sure it's committed to your GitHub repo in the same folder as app.py."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            result = {}
            for entry in data:
                if isinstance(entry, dict) and "ID" in entry and "skin" in entry:
                    result[entry["ID"]] = entry["skin"]
            if not result:
                return None, "JSON list found but no valid {ID, skin} entries detected."
            return result, None

        if isinstance(data, dict):
            return data, None

        return None, "Unrecognised JSON structure. Expected a list of {ID, skin} objects or a flat {id: name} dict."

    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"


ITEMS, load_error = load_items()


# -----------------------
# Helpers
# -----------------------
def parse_item_name(name: str):
    """Split 'Weapon | Skin' into (weapon, skin). Falls back gracefully."""
    if " | " in name:
        parts = name.split(" | ", 1)
        return parts[0].strip(), parts[1].strip()
    return name, ""


def get_weapon_types():
    if not ITEMS:
        return []
    weapons = sorted(set(parse_item_name(n)[0] for n in ITEMS.values()))
    return weapons


# -----------------------
# Early error stop (before anything tries to use ITEMS)
# -----------------------
if load_error:
    st.markdown(f'<div class="error-box">⚠ {load_error}<br><br>Make sure <code>gitskins.json</code> is committed to your GitHub repo in the same folder as <code>app.py</code>.</div>', unsafe_allow_html=True)
    st.stop()

# -----------------------
# Sidebar
# -----------------------
st.sidebar.markdown("### 🔍 Filters")

weapon_filter = []
weapon_types = get_weapon_types()
weapon_filter = st.sidebar.multiselect(
    "Weapon type",
    options=weapon_types,
    placeholder="All weapons"
)

sort_option = st.sidebar.selectbox(
    "Sort by",
    ["Name A–Z", "Name Z–A", "ID A–Z", "ID Z–A"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Quality Codes")
st.sidebar.markdown("""
<div class="quality-block">
<span class="q-title">STATTRAK + SOUVENIR</span>
<span class="q-fn">46 FN</span> · <span class="q-mw">36 MW</span> · <span class="q-ft">26 FT</span> · <span class="q-ww">16 WW</span> · <span class="q-bs">06 BS</span>

<span class="q-title">STATTRAK</span>
<span class="q-fn">44 FN</span> · <span class="q-mw">34 MW</span> · <span class="q-ft">24 FT</span> · <span class="q-ww">14 WW</span> · <span class="q-bs">04 BS</span>

<span class="q-title">SOUVENIR</span>
<span class="q-fn">42 FN</span> · <span class="q-mw">32 MW</span> · <span class="q-ft">22 FT</span> · <span class="q-ww">12 WW</span> · <span class="q-bs">02 BS</span>

<span class="q-title">STANDARD</span>
<span class="q-fn">40 FN</span> · <span class="q-mw">30 MW</span> · <span class="q-ft">20 FT</span> · <span class="q-ww">10 WW</span> · <span class="q-bs">00 BS</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#334;font-family:Share Tech Mono,monospace;font-size:0.75rem;'>by Marco🥒</p>",
    unsafe_allow_html=True
)


# -----------------------
# Main Content
# -----------------------
st.markdown('<div class="main-title">Skin Filter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">// gitskins.json · item ID lookup</div>', unsafe_allow_html=True)

# Error state
if load_error:
    st.markdown(f'<div class="error-box">⚠ {load_error}</div>', unsafe_allow_html=True)
    st.stop()

# Search bar
query = st.text_input("", placeholder="Search by ID, weapon name, or skin name…").strip().lower()

# -----------------------
# Filter + Sort
# -----------------------
filtered = []
for item_id, name in ITEMS.items():
    weapon, skin = parse_item_name(name)

    # Weapon type filter
    if weapon_filter and weapon not in weapon_filter:
        continue

    # Text search
    if query and query not in f"{item_id} {name}".lower():
        continue

    filtered.append((item_id, name, weapon, skin))

# Sort
sort_key = {
    "Name A–Z": lambda x: x[1].lower(),
    "Name Z–A": lambda x: x[1].lower(),
    "ID A–Z":   lambda x: x[0].lower(),
    "ID Z–A":   lambda x: x[0].lower(),
}
reverse = "Z–A" in sort_option
filtered.sort(key=sort_key[sort_option], reverse=reverse)

# -----------------------
# Stats bar
# -----------------------
total = len(ITEMS)
showing = len(filtered)
unique_weapons = len(set(w for _, _, w, _ in filtered))

st.markdown(f"""
<div class="stats-bar">
    <div class="stat-badge">Total items: <span>{total}</span></div>
    <div class="stat-badge">Showing: <span>{showing}</span></div>
    <div class="stat-badge">Weapons: <span>{unique_weapons}</span></div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# Results
# -----------------------
if not filtered:
    st.markdown('<div class="no-results">// no items match your query</div>', unsafe_allow_html=True)
else:
    for item_id, name, weapon, skin in filtered:
        if skin:
            display_name = f'<span class="item-weapon">{weapon}</span><span class="separator">|</span><span class="item-skin">{skin}</span>'
        else:
            display_name = f'<span class="item-skin">{name}</span>'

        st.markdown(f"""
        <div class="item-card">
            <span class="item-id">{item_id}</span>
            <span class="item-name">{display_name}</span>
        </div>
        """, unsafe_allow_html=True)

# -----------------------
# Export box
# -----------------------
if filtered:
    st.markdown("<hr>", unsafe_allow_html=True)
    with st.expander("📋 Export visible IDs"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_area(
                "IDs only",
                value="\n".join(i for i, *_ in filtered),
                height=120,
                key="export_ids"
            )
        with col2:
            st.text_area(
                "ID → Name",
                value="\n".join(f"{i}  →  {n}" for i, n, *_ in filtered),
                height=120,
                key="export_full"
            )
