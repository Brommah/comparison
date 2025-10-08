#!/bin/bash

# CEF Competitive Analysis Automation Startup Script

echo "🚀 Starting CEF Competitive Analysis Automation System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make automation script executable
chmod +x automation_system.py
chmod +x automation_server.py

# Create necessary directories
mkdir -p scraped_data
mkdir -p logs

# Start the automation server
echo "🌐 Starting web interface on http://localhost:5000"
echo "📊 Open your browser and navigate to http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"

python3 automation_server.py
