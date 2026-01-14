import os
from dotenv import load_dotenv

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = os.getenv("FMP_BASE_URL", "https://financialmodelingprep.com")

if not FMP_API_KEY:
    raise RuntimeError("FMP_API_KEY is not set in environment variables")