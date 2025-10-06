#!/bin/bash

echo "🏥 Medical Device Incidents Dashboard Setup"
echo "==========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Navigate to dashboard directory
cd /Users/Dell/Desktop/CanadianMedicalDevices/dashboard

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create data directory for CSV files
mkdir -p public/data

# Copy extracted data if it exists
if [ -f "../medical_device_incidents_enhanced_sept2024_sept2025.csv" ]; then
    echo "📊 Copying extracted data..."
    cp "../medical_device_incidents_enhanced_sept2024_sept2025.csv" public/data/
    echo "✅ Data copied successfully"
fi

echo ""
echo "🚀 Setup complete! Starting the dashboard..."
echo ""
echo "The dashboard will open at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm start