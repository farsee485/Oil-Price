import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OIL_PRICE_API_KEY = os.getenv("OIL_PRICE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Oil price API endpoint (example – adjust to your provider)
OIL_PRICE_URL = "https://api.oilpriceapi.com/v1/prices/latest"

# Refinery constants
MAX_BARRELS = 1_000_000
DEFAULT_REFINING_FEE_PER_BARREL = 5.0  # USD

# Product yield percentages (simple model)
YIELDS = {
    "Gasoline": 0.45,
    "Diesel": 0.30,
    "Jet Fuel": 0.10,
    "Heavy Fuel Oil": 0.08,
    "LPG": 0.05,
    "Other": 0.02,
}

# Product prices (mock, replace with real API if available)
PRODUCT_PRICES = {
    "Gasoline": 85.0,      # USD per barrel
    "Diesel": 90.0,
    "Jet Fuel": 88.0,
    "Heavy Fuel Oil": 60.0,
    "LPG": 70.0,
    "Other": 50.0,
}

# Database file
DB_FILE = "history.db"
