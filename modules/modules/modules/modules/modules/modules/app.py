import gradio as gr
import pandas as pd
from modules import oil_price, refinery, product_prices, database, charts, deepseek_chat
from config import MAX_BARRELS, DEFAULT_REFINING_FEE_PER_BARREL

# Initialize database
database.init_db()

# Global variable to store last calculation for chart updates
last_yield_df = None
last_prices = None

def update_price_display():
    price = oil_price.get_live_price()
    return f"**Live Oil Price:** ${price:.2f} per barrel"

def calculate(crude_barrels, fee_per_barrel, save_history):
    global last_yield_df, last_prices

    oil_price_value = oil_price.get_live_price()
    yield_df = refinery.calculate_yields(crude_barrels)
    prices = product_prices.get_product_prices()
    total_refining_fee = crude_barrels * fee_per_barrel
    total_value = refinery.calculate_total_value(yield_df, prices, total_refining_fee)

    last_yield_df = yield_df
    last_prices = prices

    # Prepare details for history
    details = {
        "yields": yield_df.to_dict(orient='records'),
        "prices": prices
    }

    if save_history:
        database.save_calculation(crude_barrels, oil_price_value, total_refining_fee, total_value, details)

    # Create yield pie chart
    pie_fig = charts.yield_pie_chart(yield_df)
    bar_fig = charts.product_values_bar_chart(yield_df, prices)

    return (
        yield_df,
        f"**Total Value after Fee:** ${total_value:,.2f}",
        pie_fig,
        bar_fig
    )

def load_history_as_df():
    df = database.get_history()
    # Convert details column to string for display
    if not df.empty:
        df['details'] = df['details'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    return df

# --- Gradio UI ---
with gr.Blocks(title="Oil Refining Calculator with AI Chat", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ⛽ Live Oil Price & Refining Calculator with AI Assistant")

    with gr.Tabs():
        # Tab 1: Calculator
        with gr.TabItem("Calculator"):
            with gr.Row():
                with gr.Column(scale=1):
                    price_display = gr.Markdown(value=update_price_display())
                    refresh_btn = gr.Button("Refresh Price")
                with gr.Column(scale=2):
                    crude_input = gr.Number(
                        label="Crude Oil (barrels)",
                        value=1000,
                        minimum=1,
                        maximum=MAX_BARRELS,
                        step=100
                    )
                    fee_input = gr.Number(
                        label="Refining Fee (USD per barrel)",
                        value=DEFAULT_REFINING_FEE_PER_BARREL,
                        minimum=0
                    )
                    save_check = gr.Checkbox(label="Save to history", value=True)
                    calc_btn = gr.Button("Calculate", variant="primary")

            with gr.Row():
                yield_table = gr.Dataframe(label="Product Yields", interactive=False)
                total_value_display = gr.Markdown()

            with gr.Row():
                pie_chart = gr.Plot(label="Yield Distribution")
                bar_chart = gr.Plot(label="Product Values")

            # Event handlers
            refresh_btn.click(fn=update_price_display, outputs=price_display)
            calc_btn.click(
                fn=calculate,
                inputs=[crude_input, fee_input, save_check],
                outputs=[yield_table, total_value_display, pie_chart, bar_chart]
            )

        # Tab 2: History & Charts
        with gr.TabItem("History & Trends"):
            gr.Markdown("### Past Calculations")
            history_table = gr.Dataframe(label="History", interactive=False)
            load_history_btn = gr.Button("Load History")
            load_history_btn.click(fn=load_history_as_df, outputs=history_table)

            gr.Markdown("### Oil Price Trend (Mock Data)")
            # For demonstration, create mock historical prices
            import datetime
            import random
            dates = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30,0,-1)]
            mock_prices = [75 + random.uniform(-5,5) for _ in range(30)]
            hist_df = pd.DataFrame({"date": dates, "price": mock_prices})
            trend_chart = gr.Plot(value=charts.price_history_chart(hist_df.to_dict('records')))
            gr.Markdown("*(Replace with real historical data from your API)*")

        # Tab 3: AI Chat (DeepSeek)
        with gr.TabItem("AI Assistant"):
            gr.Markdown("### Ask anything about oil prices, refining, or calculations")
            chatbot = gr.Chatbot(label="DeepSeek Chat")
            msg = gr.Textbox(label="Your question", placeholder="Type your question here...")
            clear = gr.Button("Clear")

            def respond(message, chat_history):
                if not message.strip():
                    return "", chat_history
                response = deepseek_chat.ask_deepseek(message, chat_history)
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": response})
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)

# Run the app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
