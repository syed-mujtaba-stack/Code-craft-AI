#!/bin/bash

# Setup script for CodeCraft AI

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Setting up CodeCraft AI...${NC}"

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo -e "❌ ${YELLOW}Python 3 is required but not installed. Please install Python 3.8 or higher and try again.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))")
if [[ "$PYTHON_VERSION" < "3.8" ]]; then
    echo -e "❌ ${YELLOW}Python 3.8 or higher is required. Found Python $PYTHON_VERSION.${NC}"
    exit 1
fi

echo -e "✓ Python $PYTHON_VERSION is installed"

# Create and activate virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "❌ ${YELLOW}Failed to create virtual environment.${NC}"
        exit 1
    fi
    echo -e "✓ Virtual environment created"
else
    echo -e "✓ Virtual environment already exists"
fi

# Activate virtual environment
if [ "$OSTYPE" = "msys" ] || [ "$OSTYPE" = "cygwin" ]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Linux/MacOS
    source venv/bin/activate
fi

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "❌ ${YELLOW}Failed to install dependencies.${NC}"
    exit 1
fi

echo -e "✓ Dependencies installed successfully"

# Set up environment variables
echo -e "\n${YELLOW}Setting up environment variables...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "✓ Created .env file from example"
    echo -e "\n${YELLOW}⚠️  Please edit the .env file and add your OpenRouter API key${NC}"
else
    echo -e "✓ .env file already exists"
fi

# Create necessary directories
echo -e "\n${YELLOW}Creating necessary directories...${NC}"
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

# Run database migrations (if any)
# echo -e "\n${YELLOW}Running database migrations...${NC}"
# alembic upgrade head

# Run tests
echo -e "\n${YELLOW}Running tests...${NC}
python -m pytest test_app.py -v

if [ $? -ne 0 ]; then
    echo -e "❌ ${YELLOW}Some tests failed. Please check the output above.${NC}
"
else
    echo -e "\n${GREEN}🎉 Setup completed successfully!${NC}"
    echo -e "\nTo start the development server, run: ${YELLOW}python manage.py run${NC}"
    echo -e "Then open your browser and go to: ${YELLOW}http://localhost:8000${NC}\n"
fi
