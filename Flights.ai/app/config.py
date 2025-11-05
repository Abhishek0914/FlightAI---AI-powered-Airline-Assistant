import os
from dotenv import load_dotenv

load_dotenv()

# Paths & API keys
MODEL_PATH = os.getenv("PHI3_MODEL_PATH", "phi3")
DB_PATH = os.getenv("DB_PATH", "data/prices.db")

# Amadeus credentials
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY", "")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET", "")
