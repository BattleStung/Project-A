#!/bin/bash

echo "🚀 AI Customer Support Assistant Launcher"
echo "=========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if dependencies are installed
if ! python3 -c "import flask" 2> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Running in DEMO MODE (no API key detected)"
    echo "   To use real AI, set: export ANTHROPIC_API_KEY='your-key'"
    echo ""
    echo "🎯 Starting demo server..."
    python3 app.py
else
    echo "✅ API key detected - using production mode"
    echo ""
    echo "🎯 Starting production server..."
    python3 app_production.py
fi