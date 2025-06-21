#!/bin/bash

echo "🚀 Legal AI Assistant - Quick Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p templates static

echo "✅ Setup complete!"
echo ""
echo "🌐 Starting the Legal AI Assistant..."
echo "   Open your browser and go to: http://localhost:8000"
echo ""
echo "📝 Example questions to try:"
echo "   - When do witness statements need to be exchanged?"
echo "   - How does the court allocate cases to a track?"
echo "   - What are the time limits for serving particulars of claim?"
echo "   - How do I make an application to strike out a statement of case?"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the application
python main.py 