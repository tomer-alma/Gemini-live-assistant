#!/bin/bash

# Gemini Live Hebrew STS - Raspberry Pi Setup Script
# This script automates the setup process for Raspberry Pi

set -e  # Exit on error

echo "======================================================"
echo "🤖 Gemini Live Hebrew STS - Raspberry Pi Setup"
echo "======================================================"
echo ""

# Detect Raspberry Pi
if [ -f /proc/device-tree/model ]; then
    PI_MODEL=$(cat /proc/device-tree/model)
    echo "✓ Detected: $PI_MODEL"
else
    echo "⚠️  Warning: Raspberry Pi not detected, continuing anyway..."
fi
echo ""

# Check Python version
echo "📍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
echo "✓ System updated"
echo ""

# Install system dependencies
echo "📥 Installing system dependencies..."
sudo apt-get install -y portaudio19-dev python3-pyaudio python3-pip python3-venv
echo "✓ System dependencies installed"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for API key
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "⚠️  .env file not found"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ Created .env from template"
        echo ""
        echo "📝 Please edit .env and add your API key:"
        echo "   1. Get API key from: https://aistudio.google.com/app/apikey"
        echo "   2. Edit .env file"
        echo "   3. Add your key: GOOGLE_API_KEY=your_key_here"
    fi
fi
echo ""

# Run tests
echo "🧪 Running tests..."
echo ""
python test_setup.py
echo ""

echo "======================================================"
echo "✅ Setup Complete!"
echo "======================================================"
echo ""
echo "Next steps:"
echo "  1. Make sure your API key is set in .env file"
echo "  2. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo "  3. Run the prototype:"
echo "     python gemini_live_hebrew.py"
echo ""
echo "Or try different personalities:"
echo "     python custom_personalities.py"
echo ""
echo "Happy prototyping! 🚀"
