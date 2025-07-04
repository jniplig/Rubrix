#!/bin/bash
echo "🎯 Rubrix Development Environment"
echo "================================"

# Start backend
cd backend
pip install -r requirements.txt
echo "🚀 Starting Rubrix API on port 8000..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Return to root
cd ..
echo "✅ Rubrix ready for development!"
echo "📱 API will be available at port 8000"
