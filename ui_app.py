import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="FinBot AI", layout="wide")

# Sidebar Authentication
st.sidebar.title("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
role = st.sidebar.selectbox("Role", ["Customer", "Admin"])

if st.sidebar.button("Login"):
    st.session_state["user"] = username
    st.session_state["role"] = role

if "user" not in st.session_state:
    st.warning("Please log in.")
    st.stop()

# --- CUSTOMER INTERFACE ---
if st.session_state["role"] == "Customer":
    st.title("💸 AI Banking Assistant")
    
    # Chat Interface
    user_input = st.text_input("Ask me anything (e.g., 'Transfer 500 to John')")
    if st.button("Send"):
        res = requests.post(f"{API_URL}/chat", params={"user_id": username, "message": user_input})
        st.write(res.json()['response'])

    st.markdown("---")
    st.subheader("Quick Actions")
    
    # Fund Transfer Form
    with st.expander("Initiate Transfer"):
        amt = st.number_input("Amount (BD)", min_value=1.0)
        iban = st.text_input("IBAN")
        country = st.selectbox("Country", ["Bahrain", "UAE", "Iran", "USA"]) # Iran included to test sanctions
        
        if st.button("Execute Transfer"):
            try:
                payload = {"user_id": username, "amount": amt, "iban": iban, "country": country}
                res = requests.post(f"{API_URL}/transfer", json=payload)
                if res.status_code == 200:
                    st.success(res.json()['message'])
                else:
                    st.error(res.json()['detail'])
            except Exception as e:
                st.error(f"Error: {e}")

# --- ADMIN INTERFACE ---
elif st.session_state["role"] == "Admin":
    st.title("🛡️ Compliance & Admin Portal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 RAG Document Ingestion")
        uploaded_file = st.file_uploader("Upload Policy PDF", type="pdf")
        if uploaded_file is not None:
            if st.button("Ingest & Retrain Model"):
                files = {'file': uploaded_file.getvalue()}
                res = requests.post(f"{API_URL}/admin/upload", files={'file': (uploaded_file.name, uploaded_file, "application/pdf")})
                st.success("Document Ingested. Vector DB Updated.")
                st.info(res.json().get('mlops_status'))

    with col2:
        st.subheader("🎫 CRM Tickets")
        # In a real app, fetch from API. Here reading DB directly for MVP speed.
        import sqlite3
        conn = sqlite3.connect('data/financial.db')
        df = pd.read_sql_query("SELECT * FROM crm_tickets", conn)
        st.dataframe(df)
        conn.close()