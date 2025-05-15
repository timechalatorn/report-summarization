import streamlit as st
import requests
import re

API_URL = "http://localhost:8000/summarize/"

st.set_page_config(page_title="Bullet Summarizer", layout="wide")
st.title("🧠 Bullet Summarizer")
st.markdown("Paste Thai text below to generate a bullet-style summary.")

user_input = st.text_area("✏️ Input Text", height=400, placeholder="วางข้อความที่นี่...")

# --- Format summary into hierarchy ---
def format_hierarchy(text):
    lines = text.strip().split("\n")
    html_lines = []

    in_overview = False

    for line in lines:
        line = line.strip()

        if not line:
            continue  # Skip blank lines

        if line.lower().startswith("overview") or "สรุป" in line.lower():
            html_lines.append(f"<div style='font-weight:bold; font-size:22px; margin-top:20px'>{line}</div>")
            in_overview = True
            continue

        if "overview" in line.lower():
            html_lines.append(f"<div style='font-weight:bold; font-size:22px; margin-top:20px'>{line}</div>")
            in_overview = False
            continue

        if "bullet summary" in line.lower():
            html_lines.append(f"<div style='font-weight:bold; font-size:22px; margin-top:30px'>{line}</div>")
            in_overview = False
            continue

        if in_overview:
            html_lines.append(f"<div style='margin-left:20px'>{line}</div>")
        elif re.match(r"^\d+\.\s", line):
            html_lines.append(f"<div style='font-weight:bold; margin-left:0px; margin-top:10px'>{line}</div>")
        elif re.match(r"^\d+\.\d+", line):
            html_lines.append(f"<div style='margin-left:20px'>{line}</div>")
        elif line.startswith("-"):
            html_lines.append(f"<div style='margin-left:40px'>{line}</div>")
        else:
            html_lines.append(f"<div style='margin-left:20px'>{line}</div>")

    return "\n".join(html_lines)


# --- Main execution ---
if st.button("🔍 Summarize") and user_input.strip():
    with st.spinner("Processing summary..."):
        try:
            response = requests.post(API_URL, json={"text": user_input})
            response.raise_for_status()
            result = response.json()

            cleaned_summary = result["final_summary"].replace("*", "")
            styled_html = format_hierarchy(cleaned_summary)

            container = f"""
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px;
                        border: 1px solid #ddd; font-size: 16px; line-height: 1.8;
                        font-family: 'sans-serif'">
            {styled_html}
            </div>
            """

            st.markdown(container, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"❌ API error: {e}")
else:
    st.info("ใส่ข้อความด้านบนแล้วกด Summarize เพื่อเริ่มต้น")
