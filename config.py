import os
from dotenv import load_dotenv

load_dotenv()

# Sqlite
DATABASE_URL = "sqlite:///carbon_credit.db"
SECRET_KEY = os.getenv("1cf39fc713abdabd7385249e18425c05")


# Supabase
SUPABASE_URL = "https://knoluipowadknsjabcqo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtub2x1aXBvd2Fka25zamFiY3FvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYxMDA0MTksImV4cCI6MjA0MTY3NjQxOX0.LDgUKgjnglG5nNQ_IH4mzmEM89McJafbFrbvhoSETSQ"
