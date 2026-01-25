from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import sqlite3
import rag_engine
import crm_agent

app = FastAPI(title="FinBot API")

class TransferRequest(BaseModel):
    user_id: str
    amount: float
    iban: str
    country: str

@app.post("/chat")
async def chat_endpoint(user_id: str, message: str):
    # 1. CRM Check (Parallel workflow)
    is_complaint, category = crm_agent.analyze_and_log_complaint(user_id, message)
    if is_complaint:
        return {"response": f"I've detected some frustration regarding {category}. A support ticket has been raised (Severity: High). An agent will contact you shortly."}

    # 2. Standard Chat Logic
    # (Simplified for MVP: In production, this would use an LLM Agent with tools)
    return {"response": f"I can help with transfers, beneficiaries, or balance checks. You said: {message}"}

@app.post("/transfer")
async def transfer_funds(req: TransferRequest):
    # 1. RAG Compliance Check
    sanctions_context = rag_engine.retrieve_rules(f"Is {req.country} sanctioned?")
    limit_context = rag_engine.retrieve_rules("What is the daily transfer limit?")
    
    # Simple keyword check simulating LLM judgment on retrieved docs
    if "sanctioned" in sanctions_context.lower() and req.country.lower() in sanctions_context.lower():
         raise HTTPException(status_code=400, detail="Transaction blocked: Destination country is sanctioned.")
         
    # 2. Balance Check (Mock API)
    conn = sqlite3.connect('data/financial.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (req.user_id,))
    row = c.fetchone()
    
    if not row or row[0] < req.amount:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient funds.")
        
    # 3. Execute
    new_bal = row[0] - req.amount
    c.execute("UPDATE users SET balance=? WHERE username=?", (new_bal, req.user_id))
    conn.commit()
    conn.close()
    
    return {"status": "success", "new_balance": new_bal, "message": "Transfer compliant and successful."}

@app.post("/admin/upload")
async def upload_document(file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Trigger MLOps Pipeline
    rag_engine.ingest_document(file_location)
    status = rag_engine.trigger_fine_tuning()
    
    return {"info": f"file '{file.filename}' processed", "mlops_status": status}
