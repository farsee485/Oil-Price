import plotly.express as px
import pandas as pd

def yield_pie_chart(yield_df):
    fig = px.pie(yield_df, values='Barrels', names='Product', title='Product Yield Distribution')
    return fig

def product_values_bar_chart(yield_df, prices):
    df = yield_df.copy()
    df['Value (USD)'] = df.apply(lambda row: row['Barrels'] * prices.get(row['Product'], 0), axis=1)
    fig = px.bar(df, x='Product', y='Value (USD)', title='Market Value by Product')
    return fig

def price_history_chart(historical_prices):
    # historical_prices: list of dicts with 'date' and 'price'
    df = pd.DataFrame(historical_prices)
    fig = px.line(df, x='date', y='price', title='Oil Price Trend (Last 30 Days)')
    return fig
