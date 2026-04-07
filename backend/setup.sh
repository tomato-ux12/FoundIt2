#!/bin/bash

# Setup script pour le backend FastAPI
# Usage: bash setup.sh

set -e  # Exit on error

echo "🚀 Setting up Idea Validator Backend..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate  # Linux/Mac
# For Windows: venv\Scripts\activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy .env if doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Supabase credentials"
fi

# Create SQL init file
echo "📋 Creating SQL initialization file..."
cat > init_db.sql << 'EOF'
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  freelance_type TEXT NOT NULL,
  years_experience INT NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Tests table
CREATE TABLE IF NOT EXISTS tests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  opportunity_id TEXT NOT NULL,
  started_at TIMESTAMP DEFAULT now(),
  completed_at TIMESTAMP,
  conversion_rate DECIMAL,
  positive_responses INT,
  total_outreach INT,
  precommits INT,
  calls_booked INT,
  notes TEXT,
  verdict TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- Index
CREATE INDEX idx_tests_user_id ON tests(user_id);
CREATE INDEX idx_tests_opportunity_id ON tests(opportunity_id);
EOF

echo "✅ SQL file created: init_db.sql"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Edit .env with your Supabase credentials"
echo "2. Copy init_db.sql to Supabase SQL editor and run it"
echo "3. Run: source venv/bin/activate && python main.py"
echo "4. Visit: http://localhost:8000/docs"
echo ""
