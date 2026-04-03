import streamlit as st
import json
from pathlib import Path

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Skin Filter",
    page_icon="🔪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------
# Custom CSS + JS
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

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #e2e8f0;
    border-bottom: 2px solid #2a7fff;
    padding-bottom: 0.4rem;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 0.9rem;
    color: #445;
    letter-spacing: 0.08em;
    margin-bottom: 1.2rem;
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

/* Clickable ID badge */
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
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
    transition: background 0.12s, border-color 0.12s, color 0.12s;
    position: relative;
}

.item-id:active {
    background: #1a3a70;
}

.item-id.copied {
    background: #0a2a1a;
    border-color: #1a7040;
    color: #4caf50;
}

.item-name {
    font-size: 1.05rem;
    font-weight: 600;
    color: #d0d8e8;
    letter-spacing: 0.03em;
    word-break: break-word;
}

.item-weapon { color: #7a8aaa; font-weight: 500; }
.item-skin   { color: #e2e8f0; }
.separator   { color: #2a7fff; margin: 0 0.3rem; }

/* Toast notification */
#copy-toast {
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: #1a3a70;
    color: #60abff;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    padding: 0.5rem 1.2rem;
    border-radius: 4px;
    border: 1px solid #2a7fff;
    opacity: 0;
    transition: opacity 0.2s, transform 0.2s;
    pointer-events: none;
    z-index: 9999;
}

#copy-toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1218;
    border-right: 1px solid #1e2330;
}

/* Stats */
.stats-bar {
    display: flex;
    gap: 0.6rem;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.stat-badge {
    background: #13161e;
    border: 1px solid #1e2330;
    border-radius: 4px;
    padding: 0.25rem 0.65rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: #7a8aaa;
}

.stat-badge span { color: #2a7fff; font-weight: 700; }

/* Quality table in main content */
.quality-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    margin: 0;
}

.quality-table th {
    color: #2a7fff;
    text-align: left;
    padding: 0.3rem 0.6rem;
    border-bottom: 1px solid #1e2330;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    white-space: nowrap;
}

.quality-table td {
    padding: 0.25rem 0.6rem;
    white-space: nowrap;
}

.quality-table tr:nth-child(even) td { background: #0f1118; }

.q-fn { color: #4caf50; }
.q-mw { color: #8bc34a; }
.q-ft { color: #ffc107; }
.q-ww { color: #ff9800; }
.q-bs { color: #f44336; }

.quality-wrap {
    background: #13161e;
    border: 1px solid #1e2330;
    border-radius: 4px;
    padding: 0.6rem 0.2rem;
    margin-bottom: 1rem;
    overflow-x: auto;
}

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

.stTextArea textarea {
    background-color: #0a0d12 !important;
    border: 1px solid #1e2330 !important;
    color: #2a7fff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}

.no-results {
    text-align: center;
    padding: 3rem;
    color: #334;
    font-size: 1rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace;
}

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

hr { border: none; border-top: 1px solid #1e2330; margin: 1rem 0; }

.stMultiSelect > div {
    background-color: #13161e !important;
    border: 1px solid #1e2330 !important;
}

/* Style st.code blocks as ID badges */
.stCode > div {
    background: #0a1428 !important;
    border: 1px solid #1a3a70 !important;
    border-radius: 3px !important;
}
.stCode code {
    color: #2a7fff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
}
.stCode button { color: #2a7fff !important; }
[data-testid="column"] {
    padding-top: 0.1rem !important;
    padding-bottom: 0.1rem !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>

<!-- Toast element -->
<div id="copy-toast">Copied!</div>

<input id="copy-helper" readonly style="position:fixed;top:-999px;left:-999px;opacity:0;width:1px;height:1px;">

<script>
function copyID(el, id) {
    var helper = document.getElementById('copy-helper');
    helper.value = id;
    helper.removeAttribute('disabled');
    helper.focus();
    helper.select();
    helper.setSelectionRange(0, 99999);

    var ok = false;
    try { ok = document.execCommand('copy'); } catch(e) {}

    if (!ok && navigator.clipboard) {
        navigator.clipboard.writeText(id).catch(function(){});
    }

    showCopied(el, id);
}

function showCopied(el, id) {
    el.classList.add('copied');
    var toast = document.getElementById('copy-toast');
    toast.textContent = 'Copied: ' + id;
    toast.classList.add('show');
    setTimeout(function() {
        el.classList.remove('copied');
        toast.classList.remove('show');
    }, 1400);
}
</script>
""", unsafe_allow_html=True)


# -----------------------
# Load JSON Data
# -----------------------
@st.cache_data
def load_items(filepath="gitskins.json"):
    if not Path(filepath).exists():
        return None, None, f"File not found: `{filepath}` — make sure it's committed to your GitHub repo in the same folder as app.py."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Format 1: {"AK-47": [{ID, skin}, ...], ...}
        if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
            result = {}
            categories = list(data.keys())
            for category, entries in data.items():
                for entry in entries:
                    if isinstance(entry, dict) and "ID" in entry and "skin" in entry:
                        result[entry["ID"]] = entry["skin"]
            if not result:
                return None, None, "Category JSON found but no valid {ID, skin} entries detected."
            return result, categories, None

        # Format 2: [{ID, skin}, ...]
        if isinstance(data, list):
            result = {}
            for entry in data:
                if isinstance(entry, dict) and "ID" in entry and "skin" in entry:
                    result[entry["ID"]] = entry["skin"]
            if not result:
                return None, None, "JSON list found but no valid {ID, skin} entries detected."
            return result, None, None

        # Format 3: {"AF": "AK-47 | Hydroponic", ...}
        if isinstance(data, dict):
            return data, None, None

        return None, None, "Unrecognised JSON structure."

    except json.JSONDecodeError as e:
        return None, None, f"JSON parse error: {e}"


ITEMS, JSON_CATEGORIES, load_error = load_items()


# -----------------------
# Helpers
# -----------------------
def parse_item_name(name: str):
    if " | " in name:
        parts = name.split(" | ", 1)
        return parts[0].strip(), parts[1].strip()
    return name, ""


def get_weapon_types():
    if not ITEMS:
        return []
    if JSON_CATEGORIES:
        return sorted(JSON_CATEGORIES)
    return sorted(set(parse_item_name(n)[0] for n in ITEMS.values()))


# -----------------------
# Sidebar (filters only)
# -----------------------
st.sidebar.markdown("### 🔍 Filters")

weapon_filter = []
weapon_types = get_weapon_types() if ITEMS else []
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
st.sidebar.markdown(
    "<p style='color:#334;font-family:Share Tech Mono,monospace;font-size:0.75rem;'>by Marco🥒</p>",
    unsafe_allow_html=True
)


# -----------------------
# Main Content
# -----------------------
st.markdown('<div class="main-title">Skin Filter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">// gitskins.json · tap an ID to copy it</div>', unsafe_allow_html=True)

# Error state
if load_error:
    st.markdown(f'<div class="error-box">⚠ {load_error}</div>', unsafe_allow_html=True)
    st.stop()

# -----------------------
# Quality Codes (always visible, collapsible)
# -----------------------
with st.expander("📋 Quality Codes", expanded=False):
    st.markdown("""
<div class="quality-wrap">
<table class="quality-table">
<tr>
  <th>TYPE</th>
  <th class="q-fn">FN</th>
  <th class="q-mw">MW</th>
  <th class="q-ft">FT</th>
  <th class="q-ww">WW</th>
  <th class="q-bs">BS</th>
</tr>
<tr>
  <td style="color:#2a7fff;font-size:0.7rem;">ST+SV</td>
  <td class="q-fn">46</td><td class="q-mw">36</td><td class="q-ft">26</td><td class="q-ww">16</td><td class="q-bs">06</td>
</tr>
<tr>
  <td style="color:#2a7fff;font-size:0.7rem;">STATTRAK</td>
  <td class="q-fn">44</td><td class="q-mw">34</td><td class="q-ft">24</td><td class="q-ww">14</td><td class="q-bs">04</td>
</tr>
<tr>
  <td style="color:#2a7fff;font-size:0.7rem;">SOUVENIR</td>
  <td class="q-fn">42</td><td class="q-mw">32</td><td class="q-ft">22</td><td class="q-ww">12</td><td class="q-bs">02</td>
</tr>
<tr>
  <td style="color:#2a7fff;font-size:0.7rem;">STANDARD</td>
  <td class="q-fn">40</td><td class="q-mw">30</td><td class="q-ft">20</td><td class="q-ww">10</td><td class="q-bs">00</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)

# Search bar
query = st.text_input("", placeholder="Search by ID, weapon name, or skin name…").strip().lower()

# -----------------------
# Filter + Sort
# -----------------------
filtered = []
for item_id, name in ITEMS.items():
    weapon, skin = parse_item_name(name)
    if weapon_filter and weapon not in weapon_filter:
        continue
    if query and query not in f"{item_id} {name}".lower():
        continue
    filtered.append((item_id, name, weapon, skin))

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
    <div class="stat-badge">Total: <span>{total}</span></div>
    <div class="stat-badge">Showing: <span>{showing}</span></div>
    <div class="stat-badge">Types: <span>{unique_weapons}</span></div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# Results
# -----------------------
if not filtered:
    st.markdown('<div class="no-results">// no items match your query</div>', unsafe_allow_html=True)
else:
    for item_id, name, weapon, skin in filtered:
        col_id, col_name = st.columns([1, 4])
        with col_id:
            st.code(item_id, language=None)
        with col_name:
            if skin:
                st.markdown(
                    f'<div class="item-name" style="padding:0.45rem 0"><span class="item-weapon">{weapon}</span><span class="separator"> | </span><span class="item-skin">{skin}</span></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="item-name" style="padding:0.45rem 0"><span class="item-skin">{name}</span></div>',
                    unsafe_allow_html=True
                )

# -----------------------
# Export box
# -----------------------
if filtered:
    st.markdown("<hr>", unsafe_allow_html=True)
    with st.expander("📤 Export visible IDs"):
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
