import pdfplumber
import docx
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


# =========================================
# 📄 EXTRACT TEXT FROM FILE
# =========================================
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([p.text for p in doc.paragraphs])

    return ""


# =========================================
# 🧹 CLEAN TEXT
# =========================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)


# =========================================
# 🔍 EXTRACT CANDIDATE DETAILS
# =========================================
def extract_details(text):
    details = {}

    # ✅ EMAIL
    email = re.findall(r'\S+@\S+', text)
    details["email"] = email[0] if email else "Not found"

    # ✅ PHONE
    phone = re.findall(r'\b\d{10}\b', text)
    details["phone"] = phone[0] if phone else "Not found"

    # ✅ NAME (first 2 words heuristic)
    lines = text.strip().split("\n")
    details["name"] = lines[0] if lines else "Not found"

    # ✅ SKILLS (basic keyword matching)
    skill_keywords = [
        "python", "machine learning", "deep learning", "sql",
        "java", "c++", "data analysis", "nlp", "tensorflow",
        "pytorch", "excel", "power bi"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill)

    details["skills"] = found_skills

    return details