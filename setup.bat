@echo off
REM Setup script for Windows

echo ⚡ Setting up CodeCraft AI...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%a in ('python -c "import sys; print('{0}.{1}'.format(sys.version_info.major, sys.version_info.minor))"') do set "PYTHON_VERSION=%%a"
if %PYTHON_VERSION% LSS 3.8 (
    echo ❌ Python 3.8 or higher is required. Found Python %PYTHON_VERSION%.
    pause
    exit /b 1
)

echo ✓ Python %PYTHON_VERSION% is installed

REM Create and activate virtual environment
echo.
echo Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install dependencies.
    pause
    exit /b 1
)

echo ✓ Dependencies installed successfully

REM Set up environment variables
echo.
echo Setting up environment variables...
if not exist ".env" (
    copy /Y .env.example .env >nul
    echo ✓ Created .env file from example
    echo.
    echo ⚠️  Please edit the .env file and add your OpenRouter API key
) else (
    echo ✓ .env file already exists
)

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "templates" mkdir templates

REM Run tests
echo.
echo Running tests...
python -m pytest test_app.py -v

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Some tests failed. Please check the output above.
    echo.
) else (
    echo.
    echo ✓ Setup completed successfully!
    echo.
    echo To start the development server, run: python manage.py run
    echo Then open your browser and go to: http://localhost:8000
    echo.
)

pause
