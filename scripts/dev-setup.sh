#!/bin/bash
echo "Setting up ConvoCanvas development environment..."

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Backend setup complete. Start with: uvicorn app.main:app --reload"
echo "Frontend setup: cd frontend && npm install && npm run dev"
