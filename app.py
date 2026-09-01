import os
import streamlit as st
from dotenv import load_dotenv
from research_agent import run_research

load_dotenv()

# Streamlit Cloud secrets fallback
try:
    if "OPENAI_API_KEY" in st.secrets and not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    if "OPENAI_MODEL" in st.secrets and not os.getenv("OPENAI_MODEL"):
        os.environ["OPENAI_MODEL"] = st.secrets["OPENAI_MODEL"]
except Exception:
    pass

st.set_page_config(
    page_title="Product Scout AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #111827;
    --blue: #3b82f6;
    --border: #e5e7eb;
    --muted: #6b7280;
    --text: #111827;
    --bg: #f7f9fc;
}

html, body, [class*="css"], .stApp {
    font-family: 'Heebo', sans-serif !important;
}

.stApp {
    background: var(--bg);
    direction: rtl;
    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    direction: rtl;
    text-align: right;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #172033 100%);
    border-left: 0;
}
section[data-testid="stSidebar"] > div { direction: rtl; }
section[data-testid="stSidebar"] * { color: #e5e7eb; }
.sidebar-logo {
    padding: 10px 4px 22px 4px;
    border-bottom: 1px solid rgba(255,255,255,.08);
    margin-bottom: 18px;
}
.sidebar-logo .brand {
    font-size: 1.28rem;
    font-weight: 800;
    color: #fff;
}
.sidebar-logo .sub {
    font-size: .78rem;
    color: #9ca3af;
    margin-top: 3px;
}
.nav-active {
    background: rgba(59,130,246,.18);
    border: 1px solid rgba(96,165,250,.28);
    color: #fff !important;
    border-radius: 12px;
    padding: 11px 13px;
    margin: 6px 0;
    font-weight: 700;
}
.nav-muted {
    color: #cbd5e1 !important;
    padding: 10px 13px;
    margin: 3px 0;
    border-radius: 10px;
}
.tip-card {
    margin-top: 28px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    padding: 14px;
    line-height: 1.55;
}
.tip-card strong { color: #fff !important; }
.tip-card span { color: #aeb9c9 !important; font-size: .82rem; }

.hero {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 30px;
    margin-bottom: 20px;
    box-shadow: 0 8px 28px rgba(17,24,39,.05);
}
.hero h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 800;
}
.hero p {
    margin: 8px 0 0 0;
    color: var(--muted);
    font-size: 1rem;
}

.section-label {
    font-size: .88rem;
    color: var(--muted);
    font-weight: 700;
    margin: 18px 0 8px;
}

div[data-testid="stRadio"] > label { display:none; }
div[data-testid="stRadio"] > div {
    display: grid !important;
    grid-template-columns: 1fr 1fr;
    gap: 14px !important;
    direction: rtl;
}
div[data-testid="stRadio"] label {
    background: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 13px 16px;
    min-height: 52px;
    transition: all .15s ease;
}
div[data-testid="stRadio"] label:hover {
    border-color: #93c5fd;
    box-shadow: 0 4px 14px rgba(59,130,246,.08);
}

.stTextArea textarea, .stTextInput input {
    direction: rtl !important;
    text-align: right !important;
    border-radius: 14px !important;
    border: 1px solid #dbe2ea !important;
    background: #fff !important;
    box-shadow: none !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.10) !important;
}

.stButton > button[kind="primary"] {
    border-radius: 13px;
    min-height: 50px;
    font-weight: 800;
    font-size: 1rem;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    border: none;
    box-shadow: 0 7px 18px rgba(37,99,235,.18);
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 12px 0 18px;
}
.source-chip {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 11px 12px;
    text-align: center;
    font-size: .88rem;
    font-weight: 600;
    color: #374151;
}

div[data-testid="stStatusWidget"] {
    border-radius: 14px;
    border: 1px solid var(--border);
    background: #fff;
}
div[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    background: white;
}

div[data-testid="stMarkdownContainer"] {
    direction: rtl;
    text-align: right;
}
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    text-align: right;
}
div[data-testid="stMarkdownContainer"] table {
    direction: rtl;
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: .9rem;
}
div[data-testid="stMarkdownContainer"] th {
    background: #f3f6fa;
    font-weight: 800;
    text-align: right !important;
}
div[data-testid="stMarkdownContainer"] th,
div[data-testid="stMarkdownContainer"] td {
    border: 1px solid #e5e7eb;
    padding: 10px 11px;
    vertical-align: top;
    text-align: right !important;
}
div[data-testid="stMarkdownContainer"] a {
    color: #2563eb;
    text-decoration: none;
}

.stDownloadButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

@media (max-width: 900px) {
    .info-grid { grid-template-columns: repeat(2, 1fr); }
    div[data-testid="stRadio"] > div { grid-template-columns: 1fr; }
    .hero { padding: 22px 20px; }
}
</style>
''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''
    <div class="sidebar-logo">
        <div class="brand">🔎 Product Scout AI</div>
        <div class="sub">מחקר מוצרים חכם</div>
    </div>
    <div class="nav-active">⌕ &nbsp; חיפוש חדש</div>
    <div class="nav-muted">◷ &nbsp; היסטוריית חיפושים</div>
    <div class="nav-muted">♡ &nbsp; מוצרים שמורים</div>
    <div class="nav-muted">⇄ &nbsp; השוואות</div>
    <div class="nav-muted">⚙ &nbsp; הגדרות</div>
    <div class="tip-card">
        <strong>💡 טיפ למחקר טוב</strong><br>
        <span>כתוב למי המוצר מיועד, טווח מחיר, שוק יעד וכל מגבלה חשובה. הסוכן יחפש בעברית ובאנגלית.</span>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('''
<div class="hero">
    <h1>מה תרצה לחפש היום?</h1>
    <p>בחר סוג חיפוש והסוכן יחפש עבורך מוצרים, ספקים, מחירים והזדמנויות בישראל ובעולם.</p>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="section-label">בחר סוג מחקר</div>', unsafe_allow_html=True)
mode = st.radio(
    "בחר סוג מחקר",
    ["🔎 מוצר ספציפי", "💡 חיפוש רעיוני"],
    horizontal=True,
    label_visibility="collapsed",
)
mode_clean = "מוצר ספציפי" if "מוצר ספציפי" in mode else "חיפוש רעיוני"

if mode_clean == "מוצר ספציפי":
    placeholder = "לדוגמה: מצא לי מכונה להכנת ארטיקים. חפש יצרנים, ספקים, מחירים, MOQ וזמינות לישראל."
else:
    placeholder = "לדוגמה: מצא לי מוצרים מעניינים למשפחות עם ילדים, עד 20 דולר מחיר מקור, שלא נפוצים בישראל."

st.markdown('<div class="section-label">מה אתה רוצה שאחקור?</div>', unsafe_allow_html=True)
query = st.text_area(
    "מה אתה רוצה שאחקור?",
    placeholder=placeholder,
    height=145,
    label_visibility="collapsed",
)

st.markdown('''
<div class="section-label">מקורות שהסוכן יבדוק</div>
<div class="info-grid">
    <div class="source-chip">🇮🇱 אתרים בישראל</div>
    <div class="source-chip">Amazon / eBay</div>
    <div class="source-chip">Alibaba / AliExpress</div>
    <div class="source-chip">🏭 יצרנים וספקים</div>
</div>
''', unsafe_allow_html=True)

with st.expander("⚙️ אפשרויות מתקדמות"):
    model = st.text_input("מודל", value=os.getenv("OPENAI_MODEL", "gpt-5.6-sol"))
    st.caption("המחקר מבקש לבדוק גם מקורות ישראליים, מרקטפלייסים, אתרי יצרנים, סיטונאים ומפיצים.")

api_key_available = bool(os.getenv("OPENAI_API_KEY"))
if not api_key_available:
    st.warning("לא נמצא OPENAI_API_KEY. יש להוסיף אותו ב-Streamlit Secrets.")

run_clicked = st.button("🚀 התחל מחקר", type="primary", use_container_width=True)

if run_clicked:
    if not query.strip():
        st.error("כתוב מה תרצה שאחקור.")
    elif not api_key_available:
        st.error("חסר OPENAI_API_KEY ב-Streamlit Secrets.")
    else:
        try:
            with st.status("הסוכן חוקר את השוק...", expanded=True) as status:
                st.write("🧭 מנסח תוכנית חיפוש בעברית ובאנגלית...")
                result = run_research(query.strip(), mode_clean, model=model.strip())
                st.write("🌐 משווה מקורות ומרכז ממצאים...")
                status.update(label="✅ המחקר הושלם", state="complete", expanded=False)

            st.markdown("### תוצאות המחקר")
            st.markdown(result["report"])

            with st.expander("🧭 תוכנית המחקר שהסוכן בנה"):
                st.markdown(result["plan"])

            st.download_button(
                "⬇️ הורד דו״ח כ-Markdown",
                data=result["report"],
                file_name="product_scout_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception as e:
            error_text = str(e)
            if "credit" in error_text.lower() or "quota" in error_text.lower():
                st.error("אין כרגע יתרת API זמינה בחשבון OpenAI. בדוק את Billing ונסה שוב לאחר שהיתרה מתעדכנת.")
            else:
                st.error("המחקר נעצר בגלל שגיאה. אפשר לשלוח לי צילום מסך ואבדוק אותה איתך.")
                with st.expander("פרטי שגיאה"):
                    st.code(error_text)

