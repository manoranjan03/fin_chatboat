import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('data/financial.db')
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, balance REAL, role TEXT)''')
    
    # Beneficiaries Table
    c.execute('''CREATE TABLE IF NOT EXISTS beneficiaries 
                 (id INTEGER PRIMARY KEY, user_id TEXT, name TEXT, iban TEXT, bank TEXT, country TEXT)''')
                 
    # CRM Table (With required columns)
    c.execute('''CREATE TABLE IF NOT EXISTS crm_tickets 
                 (id INTEGER PRIMARY KEY, user_id TEXT, complaint_text TEXT, 
                  severity TEXT, category TEXT, status TEXT)''')

    # Seed Data
    try:
        c.execute("INSERT INTO users VALUES ('john', 'pass123', 5000.0, 'customer')")
        c.execute("INSERT INTO users VALUES ('admin', 'admin123', 0.0, 'admin')")
    except sqlite3.IntegrityError:
        pass # Already exists

    conn.commit()
    conn.close()
    print("Database Initialized.")

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    init_db()
