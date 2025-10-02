# 🚀 Deployment Guide for LSTM Stock Price Predictor

This guide will help you deploy your LSTM Stock Price Predictor to Hugging Face Spaces with a Gradio interface.

## 📋 Prerequisites

Before deploying, make sure you have:

1. **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Git**: Install Git on your system
3. **Python 3.8+**: Make sure Python is installed
4. **Trained Model**: The `lstm_stock_model.h5` file should be in the `model/` directory

## 🛠️ Step-by-Step Deployment

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Test Locally (Recommended)

```bash
python test_app.py
```

This will:
- Test all imports
- Verify model loading
- Test data fetching
- Validate prediction functions
- Optionally run the app locally

### Step 3: Manual Deployment to Hugging Face Spaces

#### Option A: Using the Deployment Script (Recommended)

```bash
python deploy_hf.py
```

Follow the prompts to:
1. Enter your Hugging Face username
2. Choose a space name
3. The script will handle the rest!

#### Option B: Manual Deployment

1. **Install Hugging Face CLI**:
   ```bash
   pip install huggingface_hub[cli]
   ```

2. **Login to Hugging Face**:
   ```bash
   huggingface-cli login
   ```

3. **Create a new Space**:
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Choose "Gradio" as the SDK
   - Set your space name and visibility

4. **Clone your space repository**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   cd YOUR_SPACE_NAME
   ```

5. **Copy files to the space directory**:
   ```bash
   # Copy main application files
   cp ../app.py .
   cp ../requirements.txt .
   
   # Copy the trained model
   mkdir -p model
   cp ../model/lstm_stock_model.h5 model/
   
   # Copy README
   cp ../README_HF.md README.md
   ```

6. **Commit and push**:
   ```bash
   git add .
   git commit -m "Initial deployment of LSTM Stock Price Predictor"
   git push
   ```

## 🔧 Configuration Files

The following files are included for deployment:

- **`app.py`**: Main Gradio application
- **`requirements.txt`**: Python dependencies
- **`README_HF.md`**: Documentation for Hugging Face
- **`config.yml`**: Hugging Face Space configuration
- **`Dockerfile`**: For containerized deployment (optional)

## 🏃‍♂️ Running Locally

To test the application locally before deployment:

```bash
python app.py
```

The app will be available at `http://localhost:7860`

## 📱 Application Features

Your deployed app will include:

### Single Day Prediction
- Enter any stock symbol (AAPL, GOOGL, TSLA, etc.)
- Specify a prediction date
- Get predicted closing price with percentage change

### Multi-Day Forecast
- Generate forecasts for up to 30 consecutive days
- Visual timeline of predictions
- Confidence indicators

### Interactive Interface
- User-friendly Gradio interface
- Real-time data fetching from Yahoo Finance
- Responsive design for mobile and desktop

## 🔍 Troubleshooting

### Common Issues:

1. **Model not found error**:
   - Ensure `lstm_stock_model.h5` is in the `model/` directory
   - Check file permissions

2. **Import errors**:
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Data fetching errors**:
   - Verify internet connection
   - Try different stock symbols
   - Check if markets are open

4. **Hugging Face deployment issues**:
   - Ensure you're logged in: `huggingface-cli whoami`
   - Check space name doesn't already exist
   - Verify file sizes (max 10GB for free accounts)

### Performance Optimization:

1. **Model Loading**:
   - Model is loaded once at startup
   - Cached for multiple predictions

2. **Data Caching**:
   - Consider implementing data caching for frequently requested stocks
   - Use session state for user-specific data

3. **Error Handling**:
   - Comprehensive error messages
   - Graceful fallbacks for API failures

## 📊 Model Information

- **Architecture**: 3-layer LSTM with dropout
- **Input**: 60 days of historical closing prices
- **Output**: Next day closing price prediction
- **Preprocessing**: MinMax scaling (0-1 normalization)
- **Training**: Trained on historical stock data

## ⚠️ Important Notes

1. **Disclaimer**: This is for educational purposes only, not financial advice
2. **Data Source**: Yahoo Finance (free tier limitations may apply)
3. **Accuracy**: Model accuracy varies with market conditions
4. **Usage Limits**: Be mindful of API rate limits

## 🆘 Support

If you encounter issues:

1. Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces)
2. Review the logs in your Hugging Face Space
3. Test locally first using `test_app.py`
4. Ensure all dependencies are correctly specified

## 📈 Next Steps

After successful deployment:

1. **Monitor Performance**: Check space analytics
2. **User Feedback**: Gather user feedback for improvements
3. **Model Updates**: Retrain model with new data periodically
4. **Feature Enhancements**: Add more visualization options

---

🎉 **Congratulations!** Your LSTM Stock Price Predictor is now ready for deployment!

Your users will be able to:
- Get real-time stock predictions
- Explore multi-day forecasts
- Access the app from anywhere
- Enjoy a professional, user-friendly interface