import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pymongo import MongoClient

# Muat variabel lingkungan
load_dotenv()
POSTGRES_URI = os.getenv("POSTGRES_URI")
MONGO_URI = os.getenv("MONGO_URI")

print("Membaca file CSV...")
df = pd.read_csv("SuperMarket Analysis.csv")

# 1. Ekstrak Data Master (PostgreSQL)
print("Mengirim data master ke PostgreSQL...")
df_master = df[['Branch', 'City']].drop_duplicates().reset_index(drop=True)
engine = create_engine(POSTGRES_URI)
df_master.to_sql('branch_master', engine, if_exists='replace', index=False)

# 2. Ekstrak Log Transaksi (MongoDB)
print("Mengirim log transaksi ke MongoDB...")
df_transaction = df[['Invoice ID', 'Branch', 'Date', 'Time', 'Sales', 'Rating']]
records = df_transaction.to_dict(orient='records')
  
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["supermarket_db"]
collection = db["transactions"]
collection.drop() 
collection.insert_many(records)

print("Proses distribusi data multi-DBMS selesai!")