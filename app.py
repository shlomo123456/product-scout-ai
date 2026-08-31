
import os
import streamlit as st
from dotenv import load_dotenv
from research_agent import run_research

load_dotenv()

st.set_page_config(page_title="Product Scout AI", page_icon="🔎", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1150px; padding-top: 2rem;}
div[data-testid="stRadio"] > div {gap: 1rem;}
</style>
""", unsafe_allow_html=True)

st.title("🔎 Product Scout AI")
st.caption("מחקר מוצרים, ספקים, מחירים ורעיונות — בישראל ובעולם")

if not os.getenv("OPENAI_API_KEY"):
    st.warning("יש להוסיף OPENAI_API_KEY לקובץ .env לפני החיפוש הראשון.")

mode = st.radio(
    "בחר סוג מחקר",
    ["מוצר ספציפי", "חיפוש רעיוני"],
    horizontal=True,
)

if mode == "מוצר ספציפי":
    placeholder = "למשל: מצא לי מתקן אוטומטי לחלוקת תרופות. חפש יצרנים, ספקים ומחירים בארץ ובחו״ל."
else:
    placeholder = "למשל: מצא לי מוצרים מעניינים למשפחות עם ילדים, עד 20 דולר מחיר מקור, שלא נפוצים בישראל."

query = st.text_area("מה אתה רוצה שאחקור?", placeholder=placeholder, height=130)

with st.expander("אפשרויות מתקדמות"):
    model = st.text_input("מודל", value=os.getenv("OPENAI_MODEL", "gpt-5.6-sol"))
    st.caption("המחקר מבקש במפורש לבדוק גם Amazon, AliExpress, Alibaba, אתרים ישראליים, יצרנים וסיטונאים.")

if st.button("🚀 התחל מחקר", type="primary", use_container_width=True):
    if not query.strip():
        st.error("כתוב מה לחפש.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("חסר OPENAI_API_KEY בקובץ .env")
    else:
        try:
            with st.status("הסוכן חוקר את השוק...", expanded=True) as status:
                st.write("מנסח תוכנית חיפוש בעברית ובאנגלית...")
                result = run_research(query.strip(), mode, model=model.strip())
                st.write("מבצע חיפוש אינטרנטי ומשווה מקורות...")
                status.update(label="המחקר הושלם", state="complete")

            with st.expander("תוכנית המחקר שהסוכן בנה"):
                st.markdown(result["plan"])

            st.subheader("דו״ח מחקר")
            st.markdown(result["report"])

            st.download_button(
                "הורד דו״ח כ-Markdown",
                data=result["report"],
                file_name="product_scout_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception as e:
            st.exception(e)
