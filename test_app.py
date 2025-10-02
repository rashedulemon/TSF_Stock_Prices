#!/usr/bin/env python3
"""
Test script for the LSTM Stock Price Predictor
Run this script to test the application locally before deployment
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Gradio: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported successfully")
        print(f"   TensorFlow version: {tf.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import TensorFlow: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        import yfinance as yf
        from sklearn.preprocessing import MinMaxScaler
        print("✅ All required packages imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import required packages: {e}")
        return False
    
    return True

def test_model_loading():
    """Test if the LSTM model can be loaded"""
    print("\nTesting model loading...")
    
    model_path = Path("model/lstm_stock_model.h5")
    if not model_path.exists():
        print(f"❌ Model file not found: {model_path}")
        return False
    
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(str(model_path))
        print("✅ Model loaded successfully")
        print(f"   Model input shape: {model.input_shape}")
        print(f"   Model output shape: {model.output_shape}")
        return True
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

def test_data_fetching():
    """Test if we can fetch stock data"""
    print("\nTesting data fetching...")
    
    try:
        import yfinance as yf
        from datetime import datetime, timedelta
        
        # Test fetching Apple stock data
        ticker = yf.Ticker("AAPL")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=70)
        
        data = ticker.history(start=start_date, end=end_date)
        
        if len(data) >= 60:
            print(f"✅ Successfully fetched {len(data)} days of data for AAPL")
            return True
        else:
            print(f"⚠️ Only {len(data)} days of data available (need at least 60)")
            return False
            
    except Exception as e:
        print(f"❌ Failed to fetch stock data: {e}")
        return False

def test_prediction_function():
    """Test the prediction function"""
    print("\nTesting prediction function...")
    
    try:
        # Import the prediction function from app.py
        sys.path.append('.')
        from app import get_stock_data_and_predict
        from datetime import datetime, timedelta
        
        # Test prediction for tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        result = get_stock_data_and_predict("AAPL", tomorrow)
        
        if "Error" not in result:
            print("✅ Prediction function works successfully")
            print("Sample output:")
            print(result[:200] + "..." if len(result) > 200 else result)
            return True
        else:
            print(f"❌ Prediction function returned error: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test prediction function: {e}")
        return False

def run_local_test():
    """Run the app locally for testing"""
    print("\nStarting local test server...")
    print("This will launch the Gradio interface in your browser.")
    print("Press Ctrl+C to stop the server.")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n✅ Local test completed")
    except Exception as e:
        print(f"❌ Failed to run local test: {e}")

def main():
    print("🧪 LSTM Stock Price Predictor - Test Suite")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        ("Import Test", test_imports),
        ("Model Loading Test", test_model_loading),
        ("Data Fetching Test", test_data_fetching),
        ("Prediction Function Test", test_prediction_function)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if not test_func():
            all_tests_passed = False
    
    print(f"\n{'='*60}")
    if all_tests_passed:
        print("🎉 All tests passed! Your app is ready for deployment.")
        
        # Ask if user wants to run local test
        response = input("\nWould you like to run the app locally for testing? (y/n): ").strip().lower()
        if response == 'y':
            run_local_test()
        
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Make sure the model file exists: model/lstm_stock_model.h5")
        print("3. Check internet connection for data fetching")

if __name__ == "__main__":
    main()