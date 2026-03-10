import pandas as pd
from config import YIELDS

def calculate_yields(crude_barrels):
    """Return DataFrame with product yields."""
    data = []
    for product, fraction in YIELDS.items():
        barrels = crude_barrels * fraction
        gallons = barrels * 42
        liters = gallons * 3.78541
        data.append({
            "Product": product,
            "Barrels": round(barrels, 2),
            "Gallons": round(gallons, 2),
            "Liters": round(liters, 2),
            "Yield %": fraction * 100,
        })
    return pd.DataFrame(data)

def calculate_total_value(yield_df, product_prices, refining_fee):
    """Compute total market value minus refining fee."""
    total = 0.0
    for _, row in yield_df.iterrows():
        product = row["Product"]
        price = product_prices.get(product, 0)
        total += row["Barrels"] * price
    return total - refining_fee
