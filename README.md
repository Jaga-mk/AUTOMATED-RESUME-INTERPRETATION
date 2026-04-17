

# An Intelligent Cognitive Framework for Automated Resume Interpretation

---

## Overview

This project is a Streamlit-based Cognitive Framework for Automated Resume Interpretation that automates the recruitment process by analyzing resumes and matching them with job descriptions using BERT-based semantic similarity.

It enables recruiters to shortlist candidates efficiently based on relevance, while applicants can upload and manage their resumes. The system integrates Natural Language Processing (NLP), machine learning, and data processing techniques to provide intelligent hiring support.

---

## Features

* Secure login and registration system
* Role-based access (Recruiter and Applicant)
* Resume parsing from PDF and DOCX files
* Text preprocessing using NLP techniques
* BERT-based semantic similarity matching
* Candidate ranking based on similarity score
* Extraction of candidate details (Name, Email, Phone, Skills)
* Support for bulk resume upload via CSV
* Interactive dashboard with visualizations

---

## Tech Stack

* Frontend: Streamlit
* Backend: Python
* Machine Learning: Sentence Transformers (BERT)
* Natural Language Processing: NLTK
* Data Processing: Pandas
* File Handling: pdfplumber, python-docx
* Similarity Metric: Cosine Similarity

---

## Project Structure

```
├── app.py                      # Main application (UI and workflow)
├── bert_model.py              # BERT similarity computation
├── utils.py                  # Text extraction and preprocessing
├── users.json                # User authentication database
├── AI_Resume_Screening.csv   # Resume dataset
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git

# Navigate to the project folder
cd your-repo-name

# Install required dependencies
pip install streamlit pandas nltk pdfplumber python-docx sentence-transformers scikit-learn
```

---

## Run the Application

```bash
streamlit run app.py
```

After running the command, open the local URL displayed in the terminal to access the application.

---

## Default Login Credentials

Sample users available in `users.json`:

Recruiter

* Username: Tharun001
* Password: Tharun001

Applicant

* Username: StudentNo1
* Password: StudentNo1@123

You can also register a new account using the application interface.

---

## How to Use

### Recruiter

1. Login as Recruiter
2. Enter job description
3. Upload resumes (optional) or use dataset
4. Click "Analyze Candidates"
5. View ranked candidates
6. Select a candidate to see detailed information

### Applicant

1. Login as Applicant
2. Upload resume (PDF/DOCX)
3. Enter job category
4. Submit resume
5. View extracted details

---

## Dataset Format

For bulk upload, the CSV file should contain at least one of the following columns:

* Resume
* resume
* resume_text
* Resume_str
* Text
* content

The system automatically detects the correct column.

---

## System Workflow

1. User logs into the system
2. Applicant uploads resume
3. System extracts and preprocesses text
4. Recruiter provides job description
5. BERT model generates embeddings
6. Cosine similarity is computed
7. Candidates are ranked based on relevance
8. Recruiter reviews detailed insights

---

## Module Description

### app.py

Handles user authentication, dashboards, dataset management, and overall application workflow.

### bert_model.py

Loads the SentenceTransformer model and computes similarity scores between resumes and job descriptions.

### utils.py

Contains functions for:

* Resume text extraction
* Text cleaning and preprocessing
* Candidate detail extraction

### users.json

Stores user credentials and roles.

---

## Output

* Ranked candidates with similarity scores
* Top candidate identification
* Visual charts for comparison
* Extracted candidate details
* Full resume preview

---

## Advantages

* Reduces manual screening effort
* Improves candidate-job matching accuracy
* Fast and scalable solution
* Easy-to-use interface

---

## Limitations

* Skill extraction is keyword-based
* Name detection uses simple heuristic
* Accuracy depends on input data quality
* Initial model loading may take time

---

## Future Enhancements

* Advanced skill extraction using deep learning
* Resume scoring with feedback
* Integration with job portals
* Cloud deployment
* Enhanced filtering (experience, education)

---

## License

This project is developed for educational and research purposes.

---

