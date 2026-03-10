import requests
import time
from config import OIL_PRICE_API_KEY, OIL_PRICE_URL

_cache = {"price": None, "timestamp": 0}
CACHE_DURATION = 60  # seconds

def get_live_price():
    """Fetch current oil price per barrel in USD, with caching."""
    now = time.time()
    if _cache["price"] and (now - _cache["timestamp"] < CACHE_DURATION):
        return _cache["price"]

    if not OIL_PRICE_API_KEY:
        # Mock price for development if no API key
        mock_price = 75.0
        _cache["price"] = mock_price
        _cache["timestamp"] = now
        return mock_price

    try:
        headers = {"Authorization": f"Token {OIL_PRICE_API_KEY}"}
        response = requests.get(OIL_PRICE_URL, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Adjust parsing to your API's response format
        price = data["data"]["price"]  # Example for OilPriceAPI
        _cache["price"] = price
        _cache["timestamp"] = now
        return price
    except Exception as e:
        print(f"Error fetching oil price: {e}")
        # Return last cached price or fallback
        return _cache["price"] if _cache["price"] else 75.0
