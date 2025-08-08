import streamlit as st
import fitz  # PyMuPDF
import re
from jinja2 import Template
import base64

st.set_page_config(page_title=" Legal Parser", layout="wide")

# --- Styling to mimic LegitQuest ---
st.markdown("""
    <style>
        .block-container {
            padding: 2rem 3rem;
        }
        .css-18e3th9 {
            padding: 1rem 1rem 10rem;
        }
        .css-10trblm {
            color: #1f2937;
            font-size: 2rem;
            font-weight: 700;
        }
        .search-section {
            display: flex;
            gap: 10px;
            margin-bottom: 2rem;
        }
        .result-card {
            background: #fff;
            padding: 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
        .result-title {
            color: #1d4ed8;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .court-info {
            color: #059669;
            font-size: 0.9rem;
        }
        .result-meta {
            color: #64748b;
            font-size: 0.85rem;
            margin-top: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("##  Legal Judgment Formatter")
st.markdown("Convert court judgment PDFs into formatted, styled HTML outputs.")

# --- HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ case_title }}</title>
  <style>
    body {
      font-family: 'Georgia', serif;
      background-color: #f9fafb;
      color: #111827;
      padding: 40px;
      line-height: 1.8;
    }
    h1, h2 {
      text-align: center;
      margin: 0;
    }
    h1 {
      font-size: 30px;
    }
    h2 {
      font-size: 26px;
      margin-bottom: 10px;
    }
    h3 {
      text-align: center;
      font-weight: normal;
      font-size: 18px;
      color: #444;
      margin-top: 5px;
    }
    .meta, .judge {
      text-align: center;
      font-size: 16px;
      color: #555;
      margin-top: 10px;
    }
    .content {
      margin-top: 40px;
    }
    .point {
      margin-bottom: 20px;
      text-align: justify;
    }
    .point-number {
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h1>{{ petitioner }}</h1>
  <h2>v.</h2>
  <h1>{{ respondent }}</h1>
  <h3>{{ court_name }}</h3>
  <div class="meta">{{ appeal_number }} | {{ date }}</div>
  <div class="judge">{{ judge }}</div>
  <div class="content">
    {% for point in points %}
    <div class="point">
      <span class="point-number">{{ loop.index }}.</span> {{ point }}
    </div>
    {% endfor %}
  </div>
</body>
</html>
"""
 

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc]).strip()

def auto_split_into_points(text):
    raw_points = re.split(r'\n{2,}|(?<=[.])\s*\n+', text)
    return [p.strip().replace('\n', ' ') for p in raw_points if len(p.strip()) > 30]

def render_html(points):
    metadata = {
        "petitioner": "WAKIA AFRIN (MINOR)",
        "respondent": "M/S NATIONAL INSURANCE CO. LTD.",
        "court_name": "SUPREME COURT OF INDIA",
        "appeal_number": "SLP (C) Nos. 15447-48 of 2024",
        "date": "01-08-2025",
        "judge": "SUDHANSHU DHULIA, J. & K. VINOD CHANDRAN, J.",
        "points": points
    }
    return Template(HTML_TEMPLATE).render(**metadata)

def download_button(html_content, filename):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="font-weight:600; color:#2563eb">📥 Download HTML</a>'

# --- UI ---
st.markdown("### 📁 Upload Your Judgment PDF")
pdf_file = st.file_uploader("Select a legal judgment PDF", type=["pdf"])

if pdf_file:
    st.success("✅ PDF uploaded successfully!")
    if st.button("🛠 Generate HTML Report"):
        with st.spinner("Processing judgment..."):
            text = extract_text_from_pdf(pdf_file)
            points = auto_split_into_points(text)
            html = render_html(points)

        st.markdown("### 📄 Extracted Judgment Preview")
        st.components.v1.html(html, height=600, scrolling=True)

        st.markdown("---")
        st.markdown(download_button(html, "judgment_output.html"), unsafe_allow_html=True)
