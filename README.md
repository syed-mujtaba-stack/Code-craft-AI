# CodeCraft AI

An AI-powered multi-language coding playground that allows users to write, test, and run code in multiple languages with AI assistance.

![CodeCraft AI Screenshot](https://via.placeholder.com/800x500.png?text=CodeCraft+AI+Screenshot)

## Features

- **Multi-language Support**: Write and run code in Python, JavaScript, HTML, and CSS
- **AI-Powered Code Generation**: Generate code using natural language prompts
- **Real-time Execution**: Run code and see the output instantly
- **Code Editor**: Syntax highlighting, auto-completion, and more
- **Responsive Design**: Works on desktop and mobile devices
- **WebSocket Support**: For real-time features

## Prerequisites

- Python 3.8 or higher
- Node.js and npm (for frontend dependencies)
- OpenRouter API key (for AI features)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [OpenRouter API key](https://openrouter.ai/)
- Node.js and npm (for frontend dependencies)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/syed-mujtaba-stack/codecraft-ai.git
   cd codecraft-ai
   ```

2. **Set up a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example .env file
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

5. **Initialize the application**
   ```bash
   python manage.py setup
   ```

## 🖥️ Running the Application

### Development Mode

Start the development server with hot-reload:

```bash
python manage.py run
```

Then open your browser and navigate to [http://localhost:8000](http://localhost:8000)

### Production Mode

For production, use a production ASGI server like Uvicorn with Gunicorn:

```bash
pip install gunicorn
```

Then run:

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
```

## 🧪 Running Tests

To run the test suite:

```bash
python manage.py test
```

## 🛠️ Development

### Project Structure

```
codecraft-ai/
├── .env                    # Environment variables
├── main.py                 # Main FastAPI application
├── api.py                  # API endpoints and WebSocket handlers
├── manage.py               # Management script
├── requirements.txt        # Python dependencies
├── test_app.py            # Test cases
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── templates/             # HTML templates
    ├── base.html
    └── index.html
```

### Available Commands

- `python manage.py run` - Start the development server
- `python manage.py test` - Run tests
- `python manage.py setup` - Set up the development environment

## 🌐 API Documentation

Once the server is running, you can access the interactive API documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🛠️ Development

### Project Structure

```
codecraft-ai/
├── .env                    # Environment variables
├── main.py                 # Main FastAPI application
├── api.py                  # API endpoints and WebSocket handlers
├── manage.py               # Management script
├── requirements.txt        # Python dependencies
├── test_app.py            # Test cases
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── templates/             # HTML templates
    ├── base.html
    └── index.html
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes | - |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |
| `DEBUG` | Debug mode | No | False |
| `SECRET_KEY` | Secret key for security | No | Randomly generated |

## Security Considerations

- Always use HTTPS in production
- Keep your API keys secure and never commit them to version control
- The code execution runs in a sandboxed environment, but additional security measures may be needed for production use

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. Create a new **branch** for your feature: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add some amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. Open a **Pull Request**

### Development Workflow

1. Create an issue describing the feature or bug fix
2. Assign the issue to yourself
3. Create a new branch for your work
4. Write tests for your changes
5. Make your changes
6. Run tests and ensure they pass
7. Submit a pull request

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep lines under 100 characters
- Write meaningful commit messages

### Testing

- Write tests for all new features and bug fixes
- Run tests before submitting a PR:
  ```bash
  python -m pytest -v
  ```
- Ensure test coverage remains high

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [CodeMirror](https://codemirror.net/) - Versatile text editor
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [OpenRouter](https://openrouter.ai/) - Unified AI API
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

## 📬 Contact

If you have any questions or feedback, feel free to open an issue or reach out to the maintainers.

---

<div align="center">
  Made with ❤️ by the Syed Mujtaba abbas
</div>

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [CodeMirror](https://codemirror.net/)
- [Tailwind CSS](https://tailwindcss.com/)
- [OpenRouter](https://openrouter.ai/)
#   C o d e - c r a f t - A I  
 