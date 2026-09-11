#!/bin/bash

# একক-ক্লিক ইনস্টলেশন স্ক্রিপ্ট (Linux/Mac)
# সমস্ত ফাইল সেটআপ এবং নির্ভরতা ইনস্টল করে

echo "================================"
echo "Quotex Signal Bot - Setup"
echo "================================"
echo ""

echo "[1/3] Python version checking..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found! Please install Python3 first."
    exit 1
fi
python3 --version
echo "OK: Python3 is installed"
echo ""

echo "[2/3] Installing dependencies..."
python3 -m pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "OK: Dependencies installed"
echo ""

echo "[3/3] Running setup script..."
python3 setup.py
echo ""

echo "================================"
echo "Setup completed successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: python3 main.py"
echo ""
