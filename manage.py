#!/usr/bin/env python
"""
Management script for the CodeCraft AI application.
"""
import os
import sys
import subprocess
import uvicorn
from pathlib import Path

def run_tests():
    """Run the test suite."""
    print("Running tests...")
    return subprocess.call(["pytest", "test_app.py", "-v"])

def run_server():
    """Run the development server."""
    print("Starting development server...")
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

def setup_environment():
    """Set up the development environment."""
    print("Setting up development environment...")
    
    # Create required directories
    Path("static").mkdir(exist_ok=True)
    Path("templates").mkdir(exist_ok=True)
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.call(["pip", "install", "-r", "requirements.txt"])
    
    print("\nSetup complete!")
    print("To start the development server, run: python manage.py run")

def main():
    """Main entry point for the management script."""
    if len(sys.argv) < 2:
        print("Usage: python manage.py [command]")
        print("\nAvailable commands:")
        print("  run     - Start the development server")
        print("  test    - Run tests")
        print("  setup   - Set up the development environment")
        return 1
    
    command = sys.argv[1]
    
    if command == "run":
        run_server()
    elif command == "test":
        return run_tests()
    elif command == "setup":
        setup_environment()
    else:
        print(f"Unknown command: {command}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
