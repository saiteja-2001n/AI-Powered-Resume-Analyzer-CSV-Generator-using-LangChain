import os
import zipfile
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from typing import List

import streamlit as st
from pypdf import PdfReader
from docx import Document

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


# ------------------ ENV SETUP ------------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ------------------ LLM SETUP ------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# ------------------ STREAMLIT CONFIG ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("🧠 AI-Powered Resume Analyzer & CSV Generator")
st.write("Upload a ZIP file containing multiple PDF/DOCX resumes.")

st.info("""
💡 **Supported:** PDF & DOCX  
❌ Old `.doc` files or scanned PDFs may fail.  
👉 If a DOCX fails: Open in Word → Save As → DOCX to fix corruption.
""")


uploaded_zip = st.file_uploader(
    "Upload ZIP file",
    type=["zip"]
)


# ------------------ TEXT EXTRACTION (PDF/DOCX) ------------------
def extract_text(file_name: str, file_bytes: bytes) -> str:
    file_name = file_name.lower()

    # ---------- PDF ----------
    if file_name.endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n\n"  # preserve layout
            return text.strip()
        except Exception:
            return ""  # unreadable PDF or image-based

    # ---------- DOCX ----------
    if file_name.endswith(".docx"):
        try:
            doc = Document(BytesIO(file_bytes))
            lines = []
            for para in doc.paragraphs:
                prefix = "• " if para.style.name.startswith("List") else ""
                lines.append(prefix + para.text)
            return "\n".join(lines).strip()
        except Exception:
            return ""  # corrupted/invalid DOCX

    return ""


# ------------------ STRUCTURED SCHEMA ------------------
class ResumeSchema(BaseModel):
    full_name: str = Field(description="Candidate full name")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    skills: List[str] = Field(description="List of skills")
    education: str = Field(description="Education details")
    experience_summary: str = Field(description="Brief experience summary")


parser = PydanticOutputParser(pydantic_object=ResumeSchema)


# ------------------ PROMPT ------------------
prompt = PromptTemplate(
    template="""
You are an AI resume analyzer. Extract key information accurately.
Respond ONLY in the given structured format.

{format_instructions}

Resume:
{resume}
""",
    input_variables=["resume"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


# ------------------ MAIN PROCESS ------------------
if uploaded_zip:
    results = []

    with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
        resume_files = [
            f for f in zip_ref.namelist()
            if f.lower().endswith((".pdf", ".docx"))
        ]

        st.write(f"📄 Found **{len(resume_files)}** resume(s) in ZIP")

        for file_name in resume_files:
            st.write(f"🔎 Processing: **{file_name}** ...")

            resume_bytes = zip_ref.read(file_name)
            resume_text = extract_text(file_name, resume_bytes)

            if not resume_text.strip():
                st.error(f"❌ Unable to read or extract text: **{file_name}**")
                continue

            try:
                response = llm.invoke(
                    prompt.format(resume=resume_text)
                )
                parsed = parser.parse(response.content)
                data = parsed.dict()
                data["file_name"] = file_name
                results.append(data)

            except Exception:
                st.error(f"🚫 Failed to analyze: **{file_name}**")

    # ------------------ CSV EXPORT ------------------
    if results:
        df = pd.DataFrame(results)
        st.success("🎉 All readable resumes processed successfully!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Extracted CSV",
            csv,
            "resume_data.csv",
            "text/csv"
        )
