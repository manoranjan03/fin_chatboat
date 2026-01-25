from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import sqlite3

llm = ChatOpenAI(temperature=0, api_key="YOUR_OPENAI_KEY")

def analyze_and_log_complaint(user_id, message):
    """
    Sub-agent that detects complaints, analyzes severity/category, 
    and logs to CRM.
    """
    # 1. Sentiment & Classification Analysis
    prompt = PromptTemplate.from_template(
        """
        Analyze the following user message: "{message}"
        
        Task 1: Determine Sentiment (-1.0 to 1.0).
        Task 2: If Sentiment < -0.2, classify as "Complaint". Otherwise "General".
        Task 3: If Complaint, determine Category (Price, Service, Product).
        Task 4: Determine Severity (Low, Medium, High).
        
        Output format strictly: IS_COMPLAINT|CATEGORY|SEVERITY
        Example: YES|Service|High or NO|None|None
        """
    )
    chain = prompt | llm
    response = chain.invoke({"message": message}).content.strip()
    
    is_complaint, category, severity = response.split("|")
    
    if is_complaint == "YES":
        # Log to DB
        conn = sqlite3.connect('data/financial.db')
        c = conn.cursor()
        c.execute("INSERT INTO crm_tickets (user_id, complaint_text, severity, category, status) VALUES (?, ?, ?, ?, ?)",
                  (user_id, message, severity, category, "Open"))
        conn.commit()
        conn.close()
        return True, category
    
    return False, None