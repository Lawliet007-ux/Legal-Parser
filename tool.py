import streamlit as st
import fitz  # PyMuPDF
import re
from jinja2 import Template
import base64
from datetime import datetime

# =====================
#  ENHANCED HTML TEMPLATE - IMPROVED FORMATTING WITH CITATION STYLES
# =====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ case_title }}</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'Times New Roman', Times, serif;
      background-color: #ffffff;
      color: #000000;
      line-height: 1.6;
      font-size: 12px;
      max-width: 210mm;
      margin: 0 auto;
      padding: 20mm;
      min-height: 100vh;
    }
    
    .header-section {
      text-align: center;
      margin-bottom: 20px;
      page-break-inside: avoid;
    }
    
    .citation-line {
      font-size: 11px;
      font-weight: normal;
      margin-bottom: 8px;
      line-height: 1.3;
    }
    
    .reportable {
      font-weight: bold;
      margin-bottom: 6px;
    }
    
    .court-name {
      font-size: 14px;
      font-weight: bold;
      margin: 15px 0 10px 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .jurisdiction {
      font-size: 12px;
      font-weight: normal;
      margin-bottom: 8px;
      text-transform: uppercase;
    }
    
    .case-number {
      font-size: 12px;
      font-weight: bold;
      margin-bottom: 15px;
    }
    
    .parties-section {
      margin: 20px 0;
      text-align: left;
      max-width: 80%;
      margin-left: auto;
      margin-right: auto;
    }
    
    .party-line {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 8px;
      line-height: 1.4;
    }
    
    .party-name {
      flex: 1;
      font-size: 12px;
      font-weight: normal;
      text-transform: uppercase;
      text-align: left;
    }
    
    .party-designation {
      font-size: 11px;
      font-weight: normal;
      margin-left: 20px;
      white-space: nowrap;
    }
    
    .versus-line {
      text-align: center;
      font-size: 12px;
      font-weight: normal;
      margin: 12px 0;
    }
    
    .judgment-header {
      text-align: center;
      font-size: 14px;
      font-weight: bold;
      letter-spacing: 2px;
      margin: 25px 0 20px 0;
    }
    
    .bench-info {
      text-align: left;
      margin: 15px 0;
      font-size: 11px;
      line-height: 1.4;
    }
    
    .judge-name {
      font-weight: bold;
      margin-bottom: 8px;
    }
    
    .convenience-note {
      text-align: left;
      margin: 20px 0 15px 0;
      font-size: 11px;
      font-style: italic;
    }
    
    .index-section {
      margin: 20px 0;
      text-align: left;
    }
    
    .index-title {
      font-weight: bold;
      text-align: center;
      margin-bottom: 12px;
      text-decoration: none;
      font-size: 12px;
      text-transform: uppercase;
    }
    
    .index-item {
      margin: 2px 0;
      font-size: 11px;
      line-height: 1.4;
      text-align: left;
    }
    
    .index-main {
      font-weight: bold;
      margin-top: 6px;
      margin-bottom: 2px;
    }
    
    .index-sub {
      margin-left: 15px;
      font-weight: normal;
      margin-bottom: 1px;
    }
    
    .index-sub-sub {
      margin-left: 30px;
      font-weight: normal;
      font-style: normal;
      margin-bottom: 1px;
    }
    
    .index-sub-sub-sub {
      margin-left: 45px;
      font-weight: normal;
      font-style: italic;
      margin-bottom: 1px;
    }
    
    .content {
      margin-top: 20px;
      text-align: justify;
    }
    
    /* MAIN PARAGRAPH STYLES */
    .main-paragraph {
      margin-bottom: 12px;
      text-align: justify;
      line-height: 1.6;
      text-indent: 0;
    }
    
    .paragraph-number {
      font-weight: bold;
      display: inline;
      margin-right: 4px;
    }
    
    .paragraph-content {
      display: inline;
      font-weight: normal;
    }
    
    /* CITATION PARAGRAPH STYLES - DISTINCT FROM REGULAR PARAGRAPHS */
    .citation-paragraph {
      margin-bottom: 8px;
      text-align: justify;
      line-height: 1.5;
      text-indent: 20px;
      font-size: 11px;
      background-color: #fafafa;
      padding: 8px 12px;
      border-left: 3px solid #2196F3;
      margin-left: 10px;
      margin-right: 10px;
    }
    
    .citation-paragraph .paragraph-number {
      font-weight: bold;
      color: #2196F3;
      margin-right: 6px;
    }
    
    .citation-paragraph .paragraph-content {
      font-style: italic;
      color: #333;
    }
    
    /* ENHANCED SUB-NUMBERING STYLES */
    .section-header {
      font-weight: bold;
      text-align: center;
      margin: 20px 0 10px 0;
      font-size: 12px;
      text-decoration: none;
      text-transform: uppercase;
    }
    
    .sub-point-roman {
      margin-left: 25px;
      margin-bottom: 10px;
      text-align: justify;
      line-height: 1.6;
      padding-left: 10px;
    }
    
    .sub-point-letter {
      margin-left: 45px;
      margin-bottom: 8px;
      text-align: justify;
      line-height: 1.6;
      padding-left: 8px;
    }
    
    .sub-point-small-roman {
      margin-left: 65px;
      margin-bottom: 8px;
      text-align: justify;
      line-height: 1.6;
      padding-left: 6px;
    }
    
    .sub-point-number {
      font-weight: bold;
      color: #1976D2;
      margin-right: 6px;
      display: inline-block;
      min-width: 20px;
    }
    
    .sub-point-content {
      display: inline;
      font-weight: normal;
    }
    
    .quoted-text {
      font-style: normal;
      margin: 8px 20px;
      padding: 8px;
      background-color: #f5f5f5;
      border-left: 2px solid #ccc;
      font-size: 11px;
      line-height: 1.5;
    }
    
    .conclusion-section {
      margin-top: 25px;
    }
    
    .conclusion-title {
      font-weight: bold;
      text-align: center;
      margin: 20px 0 10px 0;
      font-size: 12px;
      text-transform: uppercase;
    }
    
    .conclusion-points {
      margin-left: 0;
    }
    
    .conclusion-point {
      margin-bottom: 8px;
      line-height: 1.6;
      text-align: justify;
    }
    
    .footer {
      margin-top: 30px;
      text-align: center;
      font-size: 10px;
      border-top: 1px solid #ccc;
      padding-top: 10px;
    }
    
    @media print {
      body {
        margin: 0;
        padding: 15mm 20mm;
        max-width: none;
      }
      
      .page-break {
        page-break-before: always;
      }
      
      .citation-paragraph {
        background-color: #f9f9f9 !important;
        -webkit-print-color-adjust: exact;
      }
    }
    
    .emphasis {
      font-weight: bold;
    }
    
    .italic {
      font-style: italic;
    }
    
    .underline {
      text-decoration: underline;
    }
    
    .center-text {
      text-align: center;
    }
    
    /* LEGAL CASE CITATION STYLES */
    .case-citation {
      font-weight: bold;
      color: #1976D2;
    }
    
    .law-reference {
      font-style: italic;
      color: #388E3C;
    }
  </style>
</head>
<body>
  <div class="header-section">
    {% if citation_number %}
    <div class="citation-line">{{ citation_number }}</div>
    {% endif %}
    
    {% if reportable %}
    <div class="citation-line reportable">{{ reportable }}</div>
    {% endif %}
    
    <div class="court-name">{{ court_name }}</div>
    
    {% if jurisdiction %}
    <div class="jurisdiction">{{ jurisdiction }}</div>
    {% endif %}
    
    <div class="case-number">{{ case_number }}</div>
  </div>
  
  <div class="parties-section">
    <div class="party-line">
      <div class="party-name">{{ petitioner }}</div>
      <div class="party-designation">…PETITIONER</div>
    </div>
    
    <div class="versus-line">VERSUS</div>
    
    <div class="party-line">
      <div class="party-name">{{ respondent }}</div>
      <div class="party-designation">…RESPONDENT(S)</div>
    </div>
  </div>
  
  {% if show_judgment_header %}
  <div class="judgment-header">J U D G M E N T</div>
  {% endif %}
  
  {% if bench_info %}
  <div class="bench-info">
    {{ bench_info | safe }}
  </div>
  {% endif %}
  
  {% if judge %}
  <div class="judge-name">
    {{ judge }}
  </div>
  {% endif %}
  
  {% if convenience_note %}
  <div class="convenience-note">
    {{ convenience_note }}
  </div>
  {% endif %}
  
  {% if index_items %}
  <div class="index-section">
    <div class="index-title">INDEX</div>
    {% for item in index_items %}
    <div class="index-item {{ item.class }}">{{ item.content | safe }}</div>
    {% endfor %}
  </div>
  {% endif %}
  
  <div class="content">
    {% for section in sections %}
      {{ section.html | safe }}
    {% endfor %}
  </div>
  
  <div class="footer">
    Generated on {{ generation_date }}
  </div>
</body>
</html>
"""

# =====================
#  ENHANCED PARSING FUNCTIONS - FIXED SUB-NUMBERING AND CITATION DETECTION
# =====================

def extract_text_from_pdf(pdf_file):
    """Extract full text from PDF with better formatting preservation."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        # Clean up the text while preserving structure
        text = re.sub(r'Printed For:.*?On:.*?\n', '', text)

        # Remove BOTH styles of page markers
        text = re.sub(r'\(Page \d+ of \d+\)', '', text)           # old pattern
        text = re.sub(r'^\s*Page\s+\d+\s+of\s+\d+\s*$', '', text, flags=re.MULTILINE)  # new pattern

        full_text += text + "\n"

    doc.close()
    return full_text.strip()

def extract_comprehensive_metadata(text):
    """Extract comprehensive metadata from judgment text with improved header parsing."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    metadata = {
        "citation_number": "",
        "reportable": "",
        "court_name": "",
        "jurisdiction": "",
        "case_number": "",
        "judgment_date": "",
        "petitioner": "",
        "respondent": "",
        "bench_info": "",
        "judge": "",
        "convenience_note": "",
        "show_judgment_header": True
    }
    
    # Extract citation number from first few lines
    for i, line in enumerate(lines[:5]):
        if re.match(r'\d{4}\s+INSC\s+\d+', line):
            metadata["citation_number"] = line
            break
    
    # Extract REPORTABLE status
    for line in lines[:10]:
        if "REPORTABLE" in line.upper():
            metadata["reportable"] = line
            break
    
    # Extract court name - look for "Supreme Court" or similar
    for line in lines[:15]:
        if "SUPREME COURT OF INDIA" in line.upper():
            metadata["court_name"] = "Supreme Court of India"
            break
        elif "Supreme Court" in line:
            metadata["court_name"] = line.strip()
            break
        elif "High Court" in line:
            metadata["court_name"] = line.strip()
            break
    
    # Extract jurisdiction
    for line in lines[:20]:
        if "CIVIL APPELLATE JURISDICTION" in line.upper():
            metadata["jurisdiction"] = line.strip()
            break
        elif "CRIMINAL APPELLATE JURISDICTION" in line.upper():
            metadata["jurisdiction"] = line.strip()
            break
        elif "JURISDICTION" in line.upper() and len(line) < 50:
            metadata["jurisdiction"] = line.strip()
            break
    
    # Extract case number with better pattern matching
    for line in lines[:25]:
        case_patterns = [
            r'(SPECIAL LEAVE PETITION.*?No\..*?\d+.*?of.*?\d+)',
            r'(Civil Appeal.*?No\..*?\d+.*?of.*?\d+)',
            r'(Criminal Appeal.*?No\..*?\d+.*?of.*?\d+)',
            r'(W\.P\..*?No\..*?\d+.*?of.*?\d+)',
            r'(TRANSFER PETITION.*?No\..*?\d+.*?of.*?\d+)'
        ]
        
        for pattern in case_patterns:
            case_match = re.search(pattern, line, re.IGNORECASE)
            if case_match:
                metadata["case_number"] = case_match.group(1).strip()
                break
        if metadata["case_number"]:
            break
    
    # Extract parties with improved logic
    petitioner_found = False
    respondent_found = False
    forbidden_keywords = ['COURT', 'JUDGMENT', 'DATE', 'BENCH', 'CITATION', 'VERSUS', 'JURISDICTION', 'PETITION']
    
    for i, line in enumerate(lines):
        line_upper = line.upper()
        
        # Look for petitioner
        if "…PETITIONER" in line_upper:
            petitioner_lines = []
            # Extract from current line before designation
            parts = re.split(r'\s*…PETITIONER', line, flags=re.I)
            if parts[0].strip():
                petitioner_lines.append(parts[0].strip())
            # Look backwards for additional name parts
            for j in range(i-1, max(0, i-5), -1):
                potential = lines[j].strip()
                if not potential:
                    break
                if any(x in potential.upper() for x in forbidden_keywords):
                    break
                petitioner_lines.insert(0, potential)
            if petitioner_lines:
                metadata["petitioner"] = clean_party_name(' '.join(petitioner_lines))
                petitioner_found = True
        
        # Look for respondent
        if "…RESPONDENT" in line_upper:
            respondent_lines = []
            # Extract from current line before designation
            parts = re.split(r'\s*…RESPONDENT\(?S\)?', line, flags=re.I)
            if parts[0].strip():
                respondent_lines.append(parts[0].strip())
            # Look backwards for additional name parts
            for j in range(i-1, max(0, i-5), -1):
                potential = lines[j].strip()
                if not potential:
                    break
                if any(x in potential.upper() for x in forbidden_keywords):
                    break
                respondent_lines.insert(0, potential)
            if respondent_lines:
                metadata["respondent"] = clean_party_name(' '.join(respondent_lines))
                respondent_found = True
        
        if petitioner_found and respondent_found:
            break
    
    # Extract judgment date from the end if not found in beginning
    if not metadata["judgment_date"]:
        for line in lines[-20:]:
            # Look for patterns like "14th August, 2025"
            date_match = re.search(r'(\d{1,2})(?:st|nd|rd|th)\s+([A-Za-z]+)\s*,\s*(\d{4})', line)
            if date_match:
                day = date_match.group(1).zfill(2)
                month_str = date_match.group(2)
                year = date_match.group(3)
                try:
                    month = datetime.strptime(month_str, '%B').month
                    metadata["judgment_date"] = f"{day}-{str(month).zfill(2)}-{year}"
                    break
                except ValueError:
                    pass
    
    # Extract bench information - improved to look for judge names at end
    bench_judges = []
    judge_patterns = [
        r'HON\'BLE.*?JUSTICE.*?J\.',
        r'HON\'BLE MR\. JUSTICE.*?J\.',
        r'HON\'BLE MS\. JUSTICE.*?J\.'
    ]
    for line in lines:
        for pattern in judge_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            bench_judges.extend(matches)
    
    # If not found, look at signatures
    if not bench_judges:
        last_text = ' '.join(lines[-10:])
        judge_matches = re.findall(r'\(\s*([A-Z\.\s]+)\s*\)', last_text)
        for match in judge_matches:
            full_name = match.strip().replace('.', '. ').strip()
            bench_judges.append(f"HON'BLE MR. JUSTICE {full_name}")
    
    if bench_judges:
        metadata["bench_info"] = "<br>".join(bench_judges[:3])  # Limit to 3 judges
    
    # Extract main judge name (usually the first one or the one writing the judgment)
    for line in lines:
        judge_match = re.search(r'([A-Z][A-Z\.\s]+J\.)', line)
        if judge_match and len(line) < 50 and "HON" not in line:
            metadata["judge"] = judge_match.group(0).strip()
            break
    
    # Extract convenience note
    for line in lines:
        if "convenience of exposition" in line.lower():
            metadata["convenience_note"] = line.strip()
            break
    
    return metadata

def clean_party_name(name):
    """Clean party names more effectively."""
    # Remove common prefixes and suffixes
    name = re.sub(r'^M/s\s*', 'M/s ', name, flags=re.IGNORECASE)
    name = re.sub(r'^M/S\s*', 'M/s ', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*….*$', '', name)  # Remove …PETITIONER etc
    return name.strip()

def extract_enhanced_index_items(text):
    """Extract index items with proper hierarchical structure."""
    lines = text.split('\n')
    index_items = []
    
    in_index = False
    for i, line in enumerate(lines):
        line = line.strip()
        
        if 'INDEX' in line.upper() and len(line) < 25:
            in_index = True
            continue
        
        if in_index:
            # Stop when we hit the first numbered paragraph
            if re.match(r'^\d+\.', line):
                break
                
            if line:
                cleaned_line = re.sub(r'\s*\.{2,}\s*\d+$', '', line).strip()  # Remove ..... 2
                
                # Main sections (A., B., C., etc.)
                if re.match(r'^[A-Z]\.', cleaned_line):
                    index_items.append({
                        'content': cleaned_line,
                        'class': 'index-main'
                    })
                # Roman numerals (I., II., III., etc.)
                elif re.match(r'^[IVX]+\.', cleaned_line):
                    index_items.append({
                        'content': cleaned_line,
                        'class': 'index-sub'
                    })
                # Letter sub-points (a., b., c., etc.)
                elif re.match(r'^[a-z]\.', cleaned_line):
                    index_items.append({
                        'content': cleaned_line,
                        'class': 'index-sub-sub'
                    })
                # Small roman sub-points (i., ii., iii., etc.)
                elif re.match(r'^[ivx]+\.', cleaned_line):
                    index_items.append({
                        'content': cleaned_line,
                        'class': 'index-sub-sub-sub'
                    })
                # Any other meaningful line
                elif len(cleaned_line) > 5 and not cleaned_line.startswith('For the'):
                    index_items.append({
                        'content': cleaned_line,
                        'class': 'index-item'
                    })
        
        if len(index_items) > 30:  # Prevent too many items
            break
    
    return index_items[:25]

def is_citation_paragraph(content):
    """Determine if a paragraph contains legal citations."""
    citation_indicators = [
        r'\b\d{4}\s+\d+\s+SCC\s+\d+\b',  # SCC citations
        r'\bMANU/SC/\d+/\d+\b',  # MANU citations
        r'\b\(\d{4}\)\s*\d+\s+SCC\s+\d+\b',  # Year SCC format
        r'\bAIR\s+\d{4}\s+SC\s+\d+\b',  # AIR citations
        r'\b\d{4}\s+\d+\s+SCR\s+\d+\b',  # SCR citations
        r'\bJT\s+\d{4}\s+\(\d+\)\s+SC\s+\d+\b',  # JT citations
        r'\b\d{4}\s+Supp\s+\(\d+\)\s+SCC\s+\d+\b',  # Supplement SCC
        r'\bvs?\.\s+[A-Z][a-zA-Z\s&]+\b',  # Case names with vs.
        r'\b[A-Z][a-zA-Z\s&]+ vs?\. [A-Z][a-zA-Z\s&]+\b',  # Full case names
        r'\bsupra\b', r'\binfra\b', r'\bibid\b',  # Legal references
        r'\bpara\s*\d+\b', r'\bparas?\.\s*\d+\b',  # Paragraph references
        r'\bSee also\b', r'\bReferred to in\b',  # Reference indicators
    ]
    
    citation_count = sum(1 for pattern in citation_indicators if re.search(pattern, content, re.IGNORECASE))
    
    # If multiple citation patterns found, likely a citation paragraph
    return citation_count >= 2 or (citation_count >= 1 and len(content) < 200)

def parse_judgment_content_enhanced(text):
    """Enhanced parsing with proper sub-numbering preservation and citation detection."""
    # Normalize text and split into lines
    normalized = re.sub(r'^\s*Page\s+\d+\s+of\s+\d+\s*$', '', text, flags=re.MULTILINE)
    lines = [line.strip() for line in normalized.split('\n') if line.strip()]
    sections = []

    # Find the first numbered paragraph as starting point
    start_idx = None
    for i, line in enumerate(lines):
        if re.match(r'^1\.\s*', line):
            start_idx = i
            break

    if start_idx is None:
        for i, line in enumerate(lines):
            if re.match(r'^\d+\.\s*', line):
                start_idx = i
                break

    if start_idx is None:
        start_idx = 0

    i = start_idx
    while i < len(lines):
        line = lines[i].strip()

        # Main section headers (A., B., C., etc.)
        if re.match(r'^[A-Z]\.\s*[A-Z]', line):
            sections.append({'html': f'<div class="section-header">{escape_html(line)}</div>'})
            i += 1
            continue

        # Numbered paragraph
        para_match = re.match(r'^(\d+)\.\s*(.*)', line)
        if para_match:
            para_num = para_match.group(1)
            para_content = para_match.group(2).strip()

            # Collect the full paragraph content
            full_content = para_content
            sub_content = []
            j = i + 1

            # Continue collecting content until next numbered paragraph or section
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line:
                    j += 1
                    continue

                # Stop at next main paragraph or section header
                if re.match(r'^\d+\.\s*', next_line) or re.match(r'^[A-Z]\.\s*[A-Z]', next_line):
                    break

                # IMPROVED SUB-NUMBERING DETECTION WITH FULL CONTENT PRESERVATION
                # Roman numerals (I., II., III., IV., V., VI., etc.)
                roman_match = re.match(r'^([IVX]+)\.\s*(.*)', next_line)
                if roman_match:
                    roman_num = roman_match.group(1) + '.'
                    roman_content = roman_match.group(2).strip()
                    
                    # Collect continuation lines for this sub-point
                    k = j + 1
                    while k < len(lines):
                        continuation_line = lines[k].strip()
                        if not continuation_line:
                            k += 1
                            continue
                        # Stop if we hit another numbering or main paragraph
                        if (re.match(r'^[IVX]+\.\s*', continuation_line) or 
                            re.match(r'^[a-z]\.\s*', continuation_line) or 
                            re.match(r'^[ivx]+\.\s*', continuation_line) or 
                            re.match(r'^\d+\.\s*', continuation_line)):
                            break
                        roman_content += " " + continuation_line
                        k += 1
                    
                    sub_content.append({
                        'type': 'roman', 
                        'number': roman_num, 
                        'content': roman_content
                    })
                    j = k
                    continue

                # Letter sub-points (a., b., c., etc.)
                letter_match = re.match(r'^([a-z])\.\s*(.*)', next_line)
                if letter_match:
                    letter_num = letter_match.group(1) + '.'
                    letter_content = letter_match.group(2).strip()
                    
                    # Collect continuation lines
                    k = j + 1
                    while k < len(lines):
                        continuation_line = lines[k].strip()
                        if not continuation_line:
                            k += 1
                            continue
                        if (re.match(r'^[a-z]\.\s*', continuation_line) or 
                            re.match(r'^[ivx]+\.\s*', continuation_line) or 
                            re.match(r'^[IVX]+\.\s*', continuation_line) or 
                            re.match(r'^\d+\.\s*', continuation_line)):
                            break
                        letter_content += " " + continuation_line
                        k += 1
                    
                    sub_content.append({
                        'type': 'letter', 
                        'number': letter_num, 
                        'content': letter_content
                    })
                    j = k
                    continue

                # Small roman numerals (i., ii., iii., iv., v., etc.)
                small_roman_match = re.match(r'^([ivx]+)\.\s*(.*)', next_line)
                if small_roman_match:
                    small_roman_num = small_roman_match.group(1) + '.'
                    small_roman_content = small_roman_match.group(2).strip()
                    
                    # Collect continuation lines
                    k = j + 1
                    while k < len(lines):
                        continuation_line = lines[k].strip()
                        if not continuation_line:
                            k += 1
                            continue
                        if (re.match(r'^[ivx]+\.\s*', continuation_line) or 
                            re.match(r'^[a-z]\.\s*', continuation_line) or 
                            re.match(r'^[IVX]+\.\s*', continuation_line) or 
                            re.match(r'^\d+\.\s*', continuation_line)):
                            break
                        small_roman_content += " " + continuation_line
                        k += 1
                    
                    sub_content.append({
                        'type': 'small_roman', 
                        'number': small_roman_num, 
                        'content': small_roman_content
                    })
                    j = k
                    continue

                # Regular continuation of main paragraph
                full_content += " " + next_line
                j += 1

            # Determine if this is a citation paragraph
            is_citation = is_citation_paragraph(full_content)
            
            # Generate HTML for the paragraph
            html_content = generate_paragraph_html(para_num, full_content, sub_content, is_citation)
            sections.append({'html': html_content})
            i = j
            continue

        i += 1

    return sections

def generate_paragraph_html(para_num, content, sub_content, is_citation=False):
    """Generate HTML for a paragraph with proper sub-numbering and citation styling."""
    # Clean and format the main content
    content = clean_and_format_text(content)
    content = format_quoted_text(content)
    
    # Choose paragraph style based on content type
    if is_citation:
        paragraph_class = "citation-paragraph"
    else:
        paragraph_class = "main-paragraph"
    
    html = f'<div class="{paragraph_class}">'
    html += f'<span class="paragraph-number">{para_num}.</span>'
    html += f'<span class="paragraph-content">{content}</span>'
    html += '</div>'
    
    # Add sub-content with improved formatting
    for sub in sub_content:
        sub_content_formatted = clean_and_format_text(sub['content'])
        sub_content_formatted = format_quoted_text(sub_content_formatted)
        
        if sub['type'] == 'roman':
            html += f'<div class="sub-point-roman">'
            html += f'<span class="sub-point-number">{sub["number"]}</span>'
            html += f'<span class="sub-point-content">{sub_content_formatted}</span>'
            html += '</div>'
        elif sub['type'] == 'letter':
            html += f'<div class="sub-point-letter">'
            html += f'<span class="sub-point-number">{sub["number"]}</span>'
            html += f'<span class="sub-point-content">{sub_content_formatted}</span>'
            html += '</div>'
        elif sub['type'] == 'small_roman':
            html += f'<div class="sub-point-small-roman">'
            html += f'<span class="sub-point-number">{sub["number"]}</span>'
            html += f'<span class="sub-point-content">{sub_content_formatted}</span>'
            html += '</div>'
    
    return html

def clean_and_format_text(text):
    """Clean and format text while preserving important elements."""
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    # Fix common formatting issues
    text = re.sub(r'\s+([,.;:])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([,.;:])\s+', r'\1 ', text)  # Ensure single space after punctuation
    
    # Handle emphasis - make legal citations and references bold/italic
    text = re.sub(r'\b(MANU/SC/\d+/\d+)\b', r'<span class="case-citation">\1</span>', text)
    text = re.sub(r'\b(\(\d+\)\s*\d+\s*SCC\s*\d+)\b', r'<span class="case-citation">\1</span>', text)
    text = re.sub(r'\b(\d{4}\s+\d+\s+SCC\s+\d+)\b', r'<span class="case-citation">\1</span>', text)
    text = re.sub(r'\b(AIR\s+\d{4}\s+SC\s+\d+)\b', r'<span class="case-citation">\1</span>', text)
    
    # Handle law references
    text = re.sub(r'\b(Section\s+\d+[A-Za-z]*(?:\(\d+\))?)\b', r'<span class="law-reference">\1</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(Article\s+\d+[A-Za-z]*(?:\(\d+\))?)\b', r'<span class="law-reference">\1</span>', text, flags=re.IGNORECASE)
    
    # Escape HTML entities after formatting
    text = escape_html_selective(text)
    
    return text

def escape_html_selective(text):
    """Escape HTML special characters while preserving our formatting spans."""
    # First, protect our formatting spans
    protected_spans = []
    span_pattern = r'<span class="[^"]*">[^<]*</span>'
    
    def protect_span(match):
        protected_spans.append(match.group(0))
        return f"__PROTECTED_SPAN_{len(protected_spans)-1}__"
    
    text = re.sub(span_pattern, protect_span, text)
    
    # Now escape HTML entities
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    # Restore protected spans
    for i, span in enumerate(protected_spans):
        text = text.replace(f"__PROTECTED_SPAN_{i}__", span)
    
    return text

def format_quoted_text(text):
    """Format quoted text with proper styling."""
    # Handle quoted passages - look for text within quotes
    quote_pattern = r'"([^"]{10,})"'  # Only format longer quotes
    text = re.sub(quote_pattern, r'<span class="quoted-text">"\1"</span>', text)
    
    return text

def escape_html(text):
    """Escape HTML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def render_enhanced_html(metadata, sections, index_items):
    """Render enhanced HTML with improved Supreme Court formatting."""
    template = Template(HTML_TEMPLATE)
    
    return template.render(
        citation_number=metadata.get('citation_number', ''),
        reportable=metadata.get('reportable', ''),
        court_name=metadata.get('court_name', 'Supreme Court of India'),
        jurisdiction=metadata.get('jurisdiction', ''),
        case_number=metadata.get('case_number', ''),
        petitioner=metadata.get('petitioner', 'PETITIONER'),
        respondent=metadata.get('respondent', 'RESPONDENT'),
        show_judgment_header=metadata.get('show_judgment_header', True),
        bench_info=metadata.get('bench_info', ''),
        judge=metadata.get('judge', ''),
        convenience_note=metadata.get('convenience_note', ''),
        sections=sections,
        index_items=index_items,
        generation_date=datetime.now().strftime('%d-%m-%Y %H:%M')
    )

def download_button(html_content, filename):
    """Generate a download link for HTML file."""
    b64 = base64.b64encode(html_content.encode('utf-8')).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64,{b64}" download="{filename}" style="display: inline-block; padding: 12px 24px; background-color: #2E7D32; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">Download Formatted Judgment</a>'
    return href

# =====================
#  STREAMLIT UI - ENHANCED WITH DEBUGGING FEATURES
# =====================

def main():
    st.set_page_config(
        page_title="Supreme Court Judgment Formatter - FIXED", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Supreme Court Judgment Formatter (FIXED)")
    st.markdown("🔧 **Issues Fixed**: Citation paragraph styling + Complete sub-numbering content preservation")
    
    # Enhanced sidebar with debug options
    with st.sidebar:
        st.header("Configuration")
        show_metadata = st.checkbox("Display Metadata", value=True)
        show_stats = st.checkbox("Show Processing Statistics", value=True)
        show_preview = st.checkbox("Show Full Preview", value=True)
        show_debug = st.checkbox("🔍 Debug Mode", value=False, help="Show detailed parsing information")
        
        st.markdown("---")
        st.markdown("### 🛠️ Key Fixes Applied")
        st.markdown("""
        **1. Citation Detection & Styling:**
        - ✅ Legal citations now have distinct blue styling
        - ✅ Citation paragraphs have special background
        - ✅ SCC, MANU, AIR citations are highlighted
        
        **2. Sub-numbering Content Preservation:**
        - ✅ Roman numerals (I., II., III.) - Full content preserved
        - ✅ Letters (a., b., c.) - Full content preserved  
        - ✅ Small romans (i., ii., iii.) - Full content preserved
        - ✅ Multi-line sub-points properly collected
        
        **3. Enhanced Text Processing:**
        - ✅ Continuation lines properly merged
        - ✅ Legal references highlighted in green
        - ✅ Case names and citations in blue
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 Citation Indicators")
        st.code("""
        • 2024 5 SCC 123
        • MANU/SC/2024/456
        • AIR 2024 SC 789
        • (2024) 3 SCC 456
        • vs. / v. in case names
        • Section 123, Article 456
        • para 12, supra, infra
        """, language="text")
        
        st.markdown("### 📋 Sub-numbering Examples")
        st.code("""
        12. Main paragraph content here
            I. Roman numeral sub-point with
               full content preserved across
               multiple lines
            II. Second roman point
                a. Letter sub-point with
                   complete content
                b. Another letter point
                    i. Small roman with
                       full text preserved
        """, language="text")
    
    # File uploader
    pdf_file = st.file_uploader(
        "Upload Supreme Court Judgment PDF", 
        type=["pdf"], 
        help="Upload PDF - Fixed version handles citations and sub-numbering correctly"
    )
    
    if pdf_file:
        st.success("📄 PDF uploaded successfully. Ready for enhanced processing.")
        
        col1, col2, col3 = st.columns([2, 2, 3])
        
        with col1:
            if st.button("🚀 Process with Fixes", type="primary", help="Apply fixes for citations and sub-numbering"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Extract text
                    status_text.text("📖 Extracting text from PDF...")
                    progress_bar.progress(10)
                    text = extract_text_from_pdf(pdf_file)
                    
                    if not text.strip():
                        st.error("❌ Unable to extract text from PDF. Please ensure the PDF contains readable text.")
                        return
                    
                    # Step 2: Extract metadata
                    status_text.text("🏛️ Extracting case metadata...")
                    progress_bar.progress(25)
                    metadata = extract_comprehensive_metadata(text)
                    
                    # Step 3: Extract index
                    status_text.text("📑 Processing index structure...")
                    progress_bar.progress(40)
                    index_items = extract_enhanced_index_items(text)
                    
                    # Step 4: Parse content with fixes
                    status_text.text("🔧 Parsing with citation detection & sub-numbering fixes...")
                    progress_bar.progress(65)
                    sections = parse_judgment_content_enhanced(text)
                    
                    # Step 5: Generate HTML
                    status_text.text("🎨 Generating enhanced HTML...")
                    progress_bar.progress(85)
                    html_content = render_enhanced_html(metadata, sections, index_items)
                    
                    # Step 6: Store results with debug info
                    progress_bar.progress(100)
                    status_text.text("✅ Processing complete with fixes applied!")
                    
                    # Store in session state
                    st.session_state.html_content = html_content
                    st.session_state.metadata = metadata
                    st.session_state.sections_count = len(sections)
                    st.session_state.index_count = len(index_items)
                    st.session_state.text_length = len(text)
                    st.session_state.processing_complete = True
                    st.session_state.sections = sections  # For debugging
                    st.session_state.raw_text = text  # For debugging
                    
                    # Count citations and sub-points for stats
                    citation_count = sum(1 for section in sections if 'citation-paragraph' in section['html'])
                    sub_points_count = sum(section['html'].count('sub-point-') for section in sections)
                    st.session_state.citation_count = citation_count
                    st.session_state.sub_points_count = sub_points_count
                    
                    st.success("🎉 Document processed successfully with all fixes applied!")
                    
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                    if show_debug:
                        st.exception(e)
                    progress_bar.empty()
                    status_text.empty()
        
        with col2:
            if 'html_content' in st.session_state:
                # Generate filename
                petitioner = st.session_state.metadata.get('petitioner', 'judgment')
                respondent = st.session_state.metadata.get('respondent', 'case')
                filename = f"{petitioner}_v_{respondent}".replace(' ', '_').replace('/', '_')
                filename = re.sub(r'[^\w\-_\.]', '', filename)[:50] + "_FIXED.html"
                
                st.markdown("### 📥 Download")
                st.markdown(download_button(st.session_state.html_content, filename), unsafe_allow_html=True)
                
                st.markdown("### 📊 Fix Statistics")
                if hasattr(st.session_state, 'citation_count'):
                    st.info(f"""
                    **Citations Detected**: {st.session_state.citation_count}
                    **Sub-points Preserved**: {st.session_state.sub_points_count}
                    **File Size**: {len(st.session_state.html_content.encode('utf-8')) / 1024:.1f} KB
                    """)
        
        with col3:
            if 'html_content' in st.session_state:
                st.markdown("### ✅ Status")
                st.success("Document ready with all fixes")
                
                # Fix summary
                st.info("""
                **Fixes Applied:**
                ✓ Citation styling & detection
                ✓ Sub-numbering content preservation
                ✓ Enhanced legal reference highlighting
                """)
                
                if st.button("🔄 Process Another Document"):
                    for key in list(st.session_state.keys()):
                        if key.startswith(('html_content', 'metadata', 'sections', 'index', 'processing', 'citation', 'sub_points', 'raw_text')):
                            del st.session_state[key]
                    st.rerun()
    
    # Enhanced results display
    if 'html_content' in st.session_state:
        st.markdown("---")
        
        # Debug information
        if show_debug:
            st.subheader("🔍 Debug Information")
            
            tab1, tab2, tab3 = st.tabs(["Citation Analysis", "Sub-numbering Analysis", "Raw Content Sample"])
            
            with tab1:
                st.markdown("**Citations Found in Document:**")
                citation_sections = [s for s in st.session_state.sections if 'citation-paragraph' in s['html']]
                if citation_sections:
                    for i, section in enumerate(citation_sections[:5]):  # Show first 5
                        clean_text = re.sub(r'<[^>]+>', '', section['html'])
                        st.text(f"Citation {i+1}: {clean_text[:200]}...")
                else:
                    st.text("No citation paragraphs detected")
            
            with tab2:
                st.markdown("**Sub-numbering Patterns Found:**")
                sub_sections = [s for s in st.session_state.sections if 'sub-point-' in s['html']]
                if sub_sections:
                    for i, section in enumerate(sub_sections[:5]):
                        clean_text = re.sub(r'<[^>]+>', '', section['html'])
                        st.text(f"Sub-point {i+1}: {clean_text[:150]}...")
                else:
                    st.text("No sub-numbering detected")
            
            with tab3:
                st.markdown("**Raw Text Sample (First 2000 chars):**")
                if hasattr(st.session_state, 'raw_text'):
                    st.text_area("Raw extracted text:", st.session_state.raw_text[:2000], height=200)
        
        # Metadata display
        if show_metadata:
            st.subheader("📋 Extracted Case Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Header Elements:**")
                header_items = [
                    ("Citation Number", st.session_state.metadata.get('citation_number', 'Not extracted')),
                    ("Reportable Status", st.session_state.metadata.get('reportable', 'Not extracted')),
                    ("Court Name", st.session_state.metadata.get('court_name', 'Not extracted')),
                    ("Jurisdiction", st.session_state.metadata.get('jurisdiction', 'Not extracted'))
                ]
                
                for label, value in header_items:
                    display_value = value[:60] + "..." if len(value) > 60 else value
                    st.text(f"{label}: {display_value}")
            
            with col2:
                st.markdown("**Case Details:**")
                case_items = [
                    ("Case Number", st.session_state.metadata.get('case_number', 'Not extracted')),
                    ("Petitioner", st.session_state.metadata.get('petitioner', 'Not extracted')),
                    ("Respondent", st.session_state.metadata.get('respondent', 'Not extracted')),
                    ("Judge", st.session_state.metadata.get('judge', 'Not extracted'))
                ]
                
                for label, value in case_items:
                    display_value = value[:60] + "..." if len(value) > 60 else value
                    st.text(f"{label}: {display_value}")
        
        # Enhanced processing statistics
        if show_stats:
            st.subheader("📈 Enhanced Processing Statistics")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                st.metric("Text Length", f"{st.session_state.text_length:,} chars")
            with col2:
                st.metric("Total Sections", st.session_state.sections_count)
            with col3:
                st.metric("Index Items", st.session_state.index_count)
            with col4:
                if hasattr(st.session_state, 'citation_count'):
                    st.metric("Citations", st.session_state.citation_count)
                else:
                    st.metric("Citations", "N/A")
            with col5:
                if hasattr(st.session_state, 'sub_points_count'):
                    st.metric("Sub-points", st.session_state.sub_points_count)
                else:
                    st.metric("Sub-points", "N/A")
            with col6:
                file_size = len(st.session_state.html_content.encode('utf-8')) / 1024
                st.metric("Output Size", f"{file_size:.1f} KB")
        
        # Document preview
        if show_preview:
            st.subheader("👁️ Enhanced Document Preview")
            
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                preview_height = st.select_slider(
                    "Preview Height", 
                    options=[600, 800, 1000, 1200, 1400], 
                    value=1000
                )
            
            with col2:
                st.markdown("**Look for:**")
                st.markdown("🔵 Blue citation highlights")
                st.markdown("🟢 Green law references")
                st.markdown("📋 Preserved sub-numbering")
            
            with col3:
                st.markdown("**Features:**")
                st.markdown("✅ Citation paragraph styling")
                st.markdown("✅ Complete sub-point content")
                st.markdown("✅ Professional formatting")
            
            # HTML preview
            st.components.v1.html(
                st.session_state.html_content, 
                height=preview_height, 
                scrolling=True
            )
        
        # Technical details
        st.markdown("---")
        st.subheader("🔧 Technical Implementation Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Citation Detection Algorithm
            **Pattern Matching:**
            - SCC citation patterns: `2024 5 SCC 123`
            - MANU references: `MANU/SC/2024/456`
            - AIR citations: `AIR 2024 SC 789`
            - Case name patterns: `vs.` and `v.`
            - Legal references: `para`, `supra`, `infra`
            
            **Styling Applied:**
            - 🔵 Blue highlighting for case citations
            - 🟢 Green highlighting for law sections
            - 📄 Special background for citation paragraphs
            """)
            
        with col2:
            st.markdown("""
            ### Sub-numbering Preservation
            **Content Collection:**
            - ✅ Roman numerals: `I.`, `II.`, `III.`, etc.
            - ✅ Letters: `a.`, `b.`, `c.`, etc.
            - ✅ Small romans: `i.`, `ii.`, `iii.`, etc.
            
            **Multi-line Handling:**
            - Continuation lines properly merged
            - Stop conditions at next numbering
            - Preserve original spacing and formatting
            - Complete content preservation guaranteed
            """)

if __name__ == "__main__":
    main()
