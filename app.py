import gradio as gr
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Load the pre-trained LSTM model
model = tf.keras.models.load_model("model/lstm_stock_model.h5")

# Initialize scaler (we'll fit it with historical data)
scaler = MinMaxScaler()

def get_stock_data_and_predict(stock_symbol, prediction_date):
    """
    Get stock data and predict closing price for a given date
    """
    try:
        # Convert prediction_date to datetime
        pred_date = datetime.strptime(prediction_date, "%Y-%m-%d")
        
        # Get historical data (we need at least 60 days of history for LSTM)
        end_date = pred_date
        start_date = end_date - timedelta(days=120)  # Get extra days to ensure we have enough data
        
        # Download stock data
        ticker = yf.Ticker(stock_symbol)
        data = ticker.history(start=start_date, end=end_date + timedelta(days=1))
        
        if len(data) < 60:
            return f"Error: Not enough historical data available for {stock_symbol}. Need at least 60 days of data."
        
        # Prepare the data similar to training
        df = data.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        df = df[['Date', 'Close']].copy()
        
        # Scale the closing prices
        close_prices = df['Close'].values.reshape(-1, 1)
        scaled_prices = scaler.fit_transform(close_prices)
        
        # Create the input sequence (last 60 days)
        if len(scaled_prices) >= 60:
            last_60_days = scaled_prices[-60:]
            last_60_days = last_60_days.reshape(1, 60, 1)
            
            # Make prediction
            prediction_scaled = model.predict(last_60_days)
            
            # Inverse transform to get actual price
            predicted_price = scaler.inverse_transform(prediction_scaled)[0][0]
            
            # Get the last actual price for reference
            last_actual_price = df['Close'].iloc[-1]
            
            
            result = f"""
            **Stock Prediction Results for {stock_symbol.upper()}**
            
            **Prediction Date**: {prediction_date}
            **Predicted Closing Price**: ${predicted_price:.2f}

            """
            
            return result
            
        else:
            return f"Error: Insufficient data for {stock_symbol}. Only {len(scaled_prices)} days available."
            
    except Exception as e:
        return f"Error: {str(e)}. Please check the stock symbol and date format."


# Create Gradio interface
with gr.Blocks(title="LSTM Stock Price Predictor", theme=gr.themes.Soft()) as iface:
    gr.Markdown(
        """
        # LSTM Stock Price Predictor

        This application uses a pre-trained LSTM neural network to predict stock closing prices based on historical data.
        
        **Features:**
        - Single day prediction
        - Real-time data fetching from Yahoo Finance
        
        **How it works:**
        The model uses the last 60 days of stock price data to predict future closing prices.
        """
    )
    
    with gr.Tab("Single Day Prediction"):
        with gr.Row():
            with gr.Column():
                stock_input = gr.Textbox(
                    label="Stock Symbol", 
                    placeholder="Enter stock symbol (e.g., AAPL, GOOGL, TSLA)",
                    value="AAPL"
                )
                date_input = gr.Textbox(
                    label="Prediction Date", 
                    placeholder="YYYY-MM-DD",
                    value=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                )
                predict_btn = gr.Button("🔮 Predict Price", variant="primary")
            
            with gr.Column():
                output = gr.Textbox(
                    label="Prediction Result", 
                    lines=10,
                    max_lines=15
                )
        
        predict_btn.click(
            fn=get_stock_data_and_predict,
            inputs=[stock_input, date_input],
            outputs=output
        )

# Launch the app
if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )
