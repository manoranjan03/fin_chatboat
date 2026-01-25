# FinBot: AI-Powered Financial Compliance Chatbot

## 📖 Project Overview
FinBot is a secure, rule-driven financial chatbot designed to facilitate fund transfers and beneficiary management while strictly enforcing compliance rules using **Retrieval-Augmented Generation (RAG)**.

This system includes:
- **Customer Interface:** For natural language banking and transaction requests.
- **Admin Portal:** For uploading compliance policies (PDFs) and monitoring RAG triggers.
- **RAG Engine:** Automatically scans transactions against uploaded sanctions/rules in a Vector Database.
- **CRM Sub-Agent:** A background process that detects negative sentiment and logs support tickets.

---

## 🏗️ Architecture & Tech Stack

- **Frontend:** Streamlit (Python-based Web UI for Customer & Admin).
- **Backend:** FastAPI (REST API for business logic & Auth).
- **AI/RAG:** LangChain + OpenAI (or Llama 3) + ChromaDB (Vector Store).
- **Database:** SQLite (Relational data for Users/Transactions).
- **DevOps:** Docker & GitHub Actions (CI/CD).

---

## 📂 Project Structure

```text
finbot/
├── data/                  # Stores SQLite DB and ChromaDB vectors
├── .github/workflows/     # CI/CD Pipeline configuration
├── main_api.py            # FastAPI Backend (Logic & Endpoints)
├── ui_app.py              # Streamlit Frontend (User & Admin Views)
├── rag_engine.py          # Document Ingestion & Retrieval Logic
├── crm_agent.py           # LangChain Agent for Complaint Analysis
├── db_setup.py            # Script to seed mock database
├── Dockerfile             # Container configuration
└── requirements.txt       # Python dependencies