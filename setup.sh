#!/bin/bash

# TOMAS Setup Script
# This script sets up both backend and frontend for TOMAS

set -e

echo "🚀 Setting up TOMAS - Task-Oriented Multi-Agent System"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the TOMAS directory
if [ ! -f "README.md" ] || [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: Must run from TOMAS root directory${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.12+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js not found. Frontend setup will be skipped.${NC}"
    SKIP_FRONTEND=true
else
    echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
    SKIP_FRONTEND=false
fi

# Setup environment file
echo ""
echo -e "${BLUE}🔑 Setting up environment...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Created .env from template. Please edit it with your API keys!${NC}"
    else
        echo -e "${RED}❌ No .env.example found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env already exists${NC}"
fi

# Backend setup
echo ""
echo -e "${BLUE}🐍 Setting up backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Deactivate virtual environment
deactivate

cd ..

# Frontend setup
if [ "$SKIP_FRONTEND" = false ]; then
    echo ""
    echo -e "${BLUE}⚛️  Setting up frontend...${NC}"
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
        echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
    else
        echo -e "${GREEN}✓ Frontend dependencies already installed${NC}"
    fi
    
    cd ..
    echo -e "${GREEN}✓ Frontend setup complete${NC}"
fi

# Final instructions
echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo -e "${YELLOW}1. Edit .env file with your API keys:${NC}"
echo "   nano .env"
echo ""
echo -e "${YELLOW}2. Start the backend:${NC}"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""

if [ "$SKIP_FRONTEND" = false ]; then
    echo -e "${YELLOW}3. In a new terminal, start the frontend:${NC}"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
fi

echo -e "${BLUE}Access:${NC}"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
if [ "$SKIP_FRONTEND" = false ]; then
    echo "   Frontend: http://localhost:3000"
fi
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
