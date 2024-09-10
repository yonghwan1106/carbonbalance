import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///carbon_credit.db"
SECRET_KEY = os.getenv("1cf39fc713abdabd7385249e18425c05")
