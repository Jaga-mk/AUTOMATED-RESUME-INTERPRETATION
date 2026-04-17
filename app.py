import streamlit as st
import pandas as pd
import json
import os

# 🔧 Import utilities
from utils import extract_text, clean_text, extract_details
from bert_model import bert_similarity

# ================================
# ⚙️ PAGE CONFIG
# ================================
st.set_page_config(
    page_title="An Intelligent Cognitive Framework for Automated Resume Interpretation",
    layout="wide"
)


# ================================
# 🔐 USER DATABASE FUNCTIONS
# ================================
USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def register_user(username, password, role):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password, "role": role}
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None

# ================================
# 🧠 SESSION SETUP
# ================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# ================================
# 🔐 LOGIN / REGISTER UI
# ================================
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if not st.session_state.logged_in:

    st.title("🔐 Secure Your Login Details")
    st.markdown("Welcome Guys!Do Not Share your Login Details with any one")

    if menu == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = login_user(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success(f"Welcome {username} ({role})")
            else:
                st.error("Invalid username or password")

    elif menu == "Register":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Recruiter", "Applicant"])

        if st.button("Register"):
            if register_user(new_user, new_pass, role):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# ================================
# 🚪 AFTER LOGIN
# ================================
role = st.session_state.role
DATA_PATH = "AI_Resume_Screening(2).csv"

st.title("🤖 AI Resume Screening System")
st.sidebar.write(f"Logged in as: {role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# =========================================
# 👨‍💼 RECRUITER DASHBOARD (FINAL WITH FILTERS)
# =========================================
if role == "Recruiter":

    st.header("👨‍💼 Recruiter Dashboard")

    job_desc = st.text_area("📝 Enter Job Description")

    uploaded_files = st.file_uploader(
        "📂 Upload Resumes (Optional)",
        accept_multiple_files=True
    )

    # =========================
    # 🔍 ANALYZE BUTTON
    # =========================
    if st.button("🔍 Analyze Candidates"):

        if job_desc.strip() == "":
            st.warning("Enter job description")
        else:
            with st.spinner("Analyzing all candidates..."):

                resumes = []
                names = []
                original_texts = []

                # =========================
                # 📁 UPLOADED FILES
                # =========================
                if uploaded_files:
                    for file in uploaded_files:
                        text = extract_text(file)
                        if not text:
                            continue
                        original_texts.append(text)
                        resumes.append(clean_text(text))
                        names.append(f"Uploaded: {file.name}")

                # =========================
                # 📂 DATASET LOADING
                # =========================
                df = pd.read_csv(DATA_PATH)

                # 🧹 Remove duplicates
                df = df.drop_duplicates(subset=["Resume"])

                # 📊 Show total candidates
                st.markdown("### 📊 Dataset Insights")
                st.write("👥 Total Candidates:", len(df))

                # 🔍 Filter by category
                if "Category" in df.columns:
                    categories = df["Category"].dropna().unique()

                    selected_category = st.selectbox(
                        "Filter by Job Category",
                        ["All"] + list(categories)
                    )

                    if selected_category != "All":
                        df = df[df["Category"] == selected_category]
                        st.write(f"📂 Showing candidates for: {selected_category}")

                # =========================
                # 📂 DATASET RESUMES LOOP
                # =========================
                for i, row in df.iterrows():
                    text = row["Resume"]

                    if pd.isna(text):
                        continue

                    text = str(text)

                    if text.strip() == "":
                        continue

                    original_texts.append(text)
                    resumes.append(clean_text(text))
                    names.append(f"Dataset Candidate {i+1}")

                # =========================
                # 🧠 BERT MATCHING
                # =========================
                job_desc_clean = clean_text(job_desc)
                scores = bert_similarity(resumes, job_desc_clean)

                results = pd.DataFrame({
                    "Candidate": names,
                    "Score": scores,
                    "Resume_Text": original_texts
                })

                results = results.sort_values(by="Score", ascending=False)

                # ✅ Save results
                st.session_state["results"] = results

            st.success("✅ Analysis Completed")

    # =========================
    # 📊 SHOW RESULTS (PERSIST)
    # =========================
    if "results" in st.session_state:

        results = st.session_state["results"]

        # 🏆 Top Candidate
        top = results.iloc[0]
        st.subheader("🏆 Top Candidate")
        st.metric(top["Candidate"], f"{top['Score']:.2f}")

        # 📊 Ranking table
        st.subheader("📊 Ranking (All Candidates)")
        st.dataframe(results[["Candidate", "Score"]], use_container_width=True)

        # 📈 Graph
        st.bar_chart(results.set_index("Candidate")["Score"])

        st.info("👇 Select a candidate below to view full details")

        st.markdown("---")
        st.markdown("## 🔍 Candidate Details")

        # 🔍 Select candidate
        selected = st.selectbox(
            "Choose Candidate",
            results["Candidate"],
            key="candidate_select"
        )

        selected_data = results[results["Candidate"] == selected].iloc[0]
        selected_resume = selected_data["Resume_Text"]

        # 🔍 Extract details
        details = extract_details(selected_resume)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 👤 Basic Info")
            st.write("👤 Name:", details["name"])
            st.write("📧 Email:", details["email"])
            st.write("📞 Phone:", details["phone"])

        with col2:
            st.markdown("### 🧠 Skills")
            st.write(", ".join(details["skills"]) if details["skills"] else "Not found")

        # 📄 Resume Preview
        st.markdown("### 📄 Resume Content")

        if selected_resume and selected_resume != "nan":
            st.text_area("Full Resume", selected_resume, height=300)
        else:
            st.warning("No resume content available")
# =========================================
# 👩‍💻 APPLICANT DASHBOARD
# =========================================
# =========================================
# 👩‍💻 APPLICANT DASHBOARD (FINAL + FULL DATA VIEW)
# =========================================
elif role == "Applicant":

    st.header("👩‍💻 Applicant Portal")

    # =========================================
    # 📄 SINGLE RESUME UPLOAD
    # =========================================
    st.subheader("📄 Upload Your Resume")

    file = st.file_uploader("Upload Resume (PDF/DOCX)")

    category = st.text_input("💼 Job Category")

    if st.button("📤 Submit Resume"):

        if file is None or category.strip() == "":
            st.warning("Please upload resume and enter category")
        else:
            text = extract_text(file)

            df = pd.read_csv(DATA_PATH)

            new_row = {
                "Category": category,
                "Resume": text
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_PATH, index=False)

            st.success("✅ Resume submitted successfully!")

            # 🔍 Extract details
            details = extract_details(text)

            st.markdown("## 📄 Extracted Candidate Details")

            col1, col2 = st.columns(2)

            with col1:
                st.write("👤 Name:", details.get("name", "Not found"))
                st.write("📧 Email:", details.get("email", "Not found"))

            with col2:
                st.write("📞 Phone:", details.get("phone", "Not found"))
                st.write("🧠 Skills:", ", ".join(details.get("skills", [])) if details.get("skills") else "Not found")

    # =========================================
    # 📂 BULK DATASET UPLOAD (FULL DISPLAY)
    # =========================================
    st.subheader("📂 Upload Multiple Resumes (CSV Dataset)")

    dataset_file = st.file_uploader("Upload CSV File", type=["csv"], key="dataset")

    if st.button("📥 Upload Dataset"):

        if dataset_file is None:
            st.warning("Please upload a CSV file")
        else:
            df = pd.read_csv(dataset_file)

            # ✅ Accept multiple possible column names
            possible_cols = ["Resume", "resume", "resume_text", "Resume_str", "Text", "content"]

            resume_col = None
            for col in possible_cols:
                if col in df.columns:
                    resume_col = col
                    break

            if resume_col is None:
                st.error("❌ No valid resume column found in CSV")
                st.write("👉 Available columns:", list(df.columns))
                st.stop()

            # ✅ Clean dataset
            df = df.dropna(subset=[resume_col])
            df = df[df[resume_col].astype(str).str.strip() != ""]

            # ✅ Rename to standard
            df = df.rename(columns={resume_col: "Resume"})

            # ✅ Merge with existing dataset
            if os.path.exists(DATA_PATH):
                existing_df = pd.read_csv(DATA_PATH)
                df = pd.concat([existing_df, df], ignore_index=True)

            df.to_csv(DATA_PATH, index=False)

            st.success(f"✅ {len(df)} resumes uploaded successfully!")

            # ✅ SHOW FULL DATASET
            st.markdown("### 📊 Full Dataset View")
            st.write("Total Records:", len(df))

            st.dataframe(df, use_container_width=True)