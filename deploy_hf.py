#!/usr/bin/env python3
"""
Deployment script for Hugging Face Spaces
This script helps you deploy the LSTM Stock Price Predictor to Hugging Face Spaces
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
    except subprocess.CalledProcessError:
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    try:
        subprocess.run(["huggingface-cli", "--version"], check=True, capture_output=True)
        print("✅ Hugging Face CLI is installed")
    except subprocess.CalledProcessError:
        print("❌ Hugging Face CLI is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub[cli]"])
    
    return True

def setup_huggingface_space(space_name, username):
    """Setup and deploy to Hugging Face Spaces"""
    
    print(f"🚀 Setting up Hugging Face Space: {username}/{space_name}")
    
    # Login to Hugging Face (if not already logged in)
    print("Please make sure you're logged in to Hugging Face:")
    print("Run: huggingface-cli login")
    input("Press Enter after you've logged in...")
    
    # Create the space
    try:
        cmd = [
            "huggingface-cli", "repo", "create", 
            f"{username}/{space_name}", 
            "--type", "space", 
            "--space_sdk", "gradio"
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Created space: {username}/{space_name}")
    except subprocess.CalledProcessError as e:
        if "already exists" in str(e):
            print(f"⚠️ Space {username}/{space_name} already exists")
        else:
            print(f"❌ Error creating space: {e}")
            return False
    
    # Clone the space repository
    space_url = f"https://huggingface.co/spaces/{username}/{space_name}"
    clone_dir = f"{space_name}_hf_space"
    
    try:
        subprocess.run(["git", "clone", space_url, clone_dir], check=True)
        print(f"✅ Cloned space repository to {clone_dir}")
    except subprocess.CalledProcessError:
        print(f"❌ Error cloning space repository")
        return False
    
    # Copy files to the space directory
    current_dir = Path(".")
    space_dir = Path(clone_dir)
    
    files_to_copy = [
        "app.py",
        "requirements.txt",
        "model/lstm_stock_model.h5",
        "README_HF.md"
    ]
    
    for file_path in files_to_copy:
        src = current_dir / file_path
        dst = space_dir / (file_path if file_path != "README_HF.md" else "README.md")
        
        if src.exists():
            # Create destination directory if it doesn't exist
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            import shutil
            shutil.copy2(src, dst)
            print(f"✅ Copied {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}")
    
    # Create README.md for the space (if not exists)
    readme_path = space_dir / "README.md"
    if not readme_path.exists():
        with open(readme_path, "w") as f:
            f.write(f"""---
title: {space_name}
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# LSTM Stock Price Predictor

AI-powered stock price prediction using LSTM neural networks.
""")
        print("✅ Created README.md")
    
    # Commit and push to Hugging Face
    os.chdir(space_dir)
    
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial deployment of LSTM Stock Price Predictor"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Pushed changes to Hugging Face Spaces")
        print(f"🎉 Your space is now available at: {space_url}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to Hugging Face: {e}")
        return False
    
    return True

def main():
    print("🏛️ LSTM Stock Price Predictor - Hugging Face Deployment")
    print("=" * 60)
    
    if not check_requirements():
        return
    
    # Get user input
    username = input("Enter your Hugging Face username: ").strip()
    space_name = input("Enter space name (e.g., lstm-stock-predictor): ").strip()
    
    if not username or not space_name:
        print("❌ Username and space name are required!")
        return
    
    # Setup and deploy
    success = setup_huggingface_space(space_name, username)
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print(f"Your app is available at: https://huggingface.co/spaces/{username}/{space_name}")
        print("\nNote: It may take a few minutes for the space to build and become available.")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")

if __name__ == "__main__":
    main()