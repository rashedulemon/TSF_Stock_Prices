---
title: LSTM Stock Price Predictor
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# LSTM Stock Price Predictor 🏛️

This application uses a pre-trained LSTM (Long Short-Term Memory) neural network to predict stock closing prices based on historical data.

## Features

- **Single Day Prediction**: Get predicted closing price for any stock on a specific date
- **Multi-Day Forecasting**: Generate forecasts for up to 30 consecutive days
- **Real-time Data**: Fetches live data from Yahoo Finance
- **User-friendly Interface**: Built with Gradio for easy interaction

## How It Works

The model uses the last 60 days of stock price data to predict future closing prices. It employs a deep LSTM architecture with:

- 3 LSTM layers with 50 units each
- Dropout layers for regularization
- MinMax scaling for data normalization
- 60-day lookback window

## Usage

1. **Single Day Prediction**:
   - Enter a stock symbol (e.g., AAPL, GOOGL, TSLA)
   - Specify the prediction date in YYYY-MM-DD format
   - Click "Predict Price" to get the forecast

2. **Multi-Day Forecast**:
   - Enter a stock symbol
   - Set the start date for predictions
   - Choose the number of days to forecast (1-30)
   - Click "Generate Forecast"

## Model Details

- **Architecture**: Deep LSTM with 3 layers
- **Training Data**: Historical stock price data
- **Input**: 60 days of closing prices
- **Output**: Next day closing price prediction
- **Preprocessing**: MinMax scaling (0-1 normalization)

## Limitations

- Predictions are based on historical patterns and may not account for sudden market changes
- Accuracy decreases for longer prediction horizons
- Should not be used as the sole basis for investment decisions

## Disclaimer

⚠️ **Important**: This tool is for educational and research purposes only. Stock market predictions are inherently uncertain, and this model's predictions should not be considered as financial advice. Always consult with financial professionals and conduct your own research before making investment decisions.

## Technical Requirements

- Python 3.8+
- TensorFlow 2.10+
- Gradio 4.0+
- scikit-learn
- pandas
- numpy
- yfinance

## License

MIT License - see LICENSE file for details.