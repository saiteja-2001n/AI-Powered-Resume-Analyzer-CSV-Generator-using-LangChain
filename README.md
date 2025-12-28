# 🧠 AI-Powered Resume Analyzer & CSV Generator

This project is an end-to-end automated resume analysis system that extracts key candidate information from PDF & DOCX resumes using LLMs (Gemini) and LangChain.
It processes multiple resumes at once (via ZIP file) and generates a structured CSV file ready for HR screening, ATS pipelines, or data analysis.

## ⭐ Features
### 📂 Bulk Resume Processing
- Upload a ZIP file containing multiple resumes in PDF or DOCX format.

## 🤖 AI-Powered Extraction

Automatically extracts:

- Full Name
- Email
- Phone Number
- Skills
- Education
- Experience Summary

## 🧾 Structured CSV Output

- Download a consolidated CSV file where each row = one candidate.

## 🖥️ Simple UI

- Built with Streamlit for a fast, user-friendly interface.

## ⚙️ Tech Stack
- Component	Technology-
- UI / Frontend	Streamlit
- LLM Pipeline	LangChain + Gemini
- Output Validation	PydanticOutputParser
- Document Parsing	PyPDF / python-docx
- Data Handling	Pandas

## 📂 Project Structure
resume-analyzer/
│── app.py              # Main Streamlit application
│── req.txt             # Dependencies list
│── .env                # API key (excluded from GitHub)
│── README.md           # Project documentation
└── files/              # (optional) supporting files

## 📌 How It Works (Process Flow)
📂 Upload ZIP
     ↓
📄 Extract text from PDF/DOCX
     ↓
🤖 Send to Gemini LLM via LangChain
     ↓
📋 Pydantic schema ensures structured output
     ↓
📊 Generate CSV for download

## 📍 Example Output (CSV)
file_name	full_name	email	phone	skills	education	experience_summary
john.pdf	John Abraham	john@mail.com
	9999988888	Python, SQL, Power BI	B.Tech (CSE)	3yrs in data analytics
priya.docx	Priya Sharma	priya@mail.com
	8888877777	React, Node, JavaScript	B.Sc Computer Science	2yrs in web development


## 🌟 Future Enhancements
- 📊 ATS scoring system
- 🎯 Job Description matching score
- ⭐ Resume ranking and scoring
- 🔎 Experience & skill categorization

