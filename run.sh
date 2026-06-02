#!/bin/bash

# QR Code Generator - Quick Start Script for macOS/Linux

echo ""
echo "================================================"
echo "  QR Code Generator - Quick Start"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        echo "Make sure Python 3 is installed"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
pip show flask > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Create necessary directories
mkdir -p static/uploads
mkdir -p static/generated_qr

# Set Flask environment
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo ""
echo "================================================"
echo "  Starting QR Code Generator..."
echo "================================================"
echo ""
echo "Application will be available at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Flask application
python app.py
