# Contributing to CodeCraft AI

Thank you for your interest in contributing to CodeCraft AI! We welcome contributions from everyone, regardless of experience level. This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check if the issue has already been reported. If you find an open issue that addresses the problem, add a comment to the existing issue instead of creating a new one.

When creating a bug report, please include the following information:

1. A clear and descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots or screen recordings if applicable
6. Your environment (OS, browser, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features and improvements. When suggesting an enhancement:

1. Use a clear and descriptive title
2. Provide a step-by-step description of the suggested enhancement
3. Explain why this enhancement would be useful
4. Include screenshots or mockups if applicable

### Your First Code Contribution

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Run tests and ensure they pass
6. Commit your changes with a descriptive commit message
7. Push your branch to your fork
8. Open a pull request

### Pull Requests

When submitting a pull request:

1. Ensure the PR description clearly describes the problem and solution
2. Include the relevant issue number if applicable
3. Make sure all tests pass
4. Update the documentation if necessary
5. Keep your PR focused on a single feature or bugfix

## Development Environment

### Prerequisites

- Python 3.8+
- Node.js and npm (for frontend dependencies)
- Git

### Setup

1. Fork and clone the repository
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration.

### Running the Application

```bash
python manage.py run
```

### Running Tests

```bash
python -m pytest
```

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep lines under 100 characters
- Use type hints for function parameters and return values

### JavaScript

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use ES6+ features where appropriate
- Use meaningful variable and function names

### HTML/CSS

- Use semantic HTML5 elements
- Follow BEM (Block Element Modifier) methodology for CSS
- Use Tailwind CSS utility classes when possible

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Here are some examples:

- `feat: add user authentication`
- `fix: resolve login issue`
- `docs: update README`
- `style: format code`
- `refactor: improve code structure`
- `test: add unit tests`
- `chore: update dependencies`

## License

By contributing to this project, you agree that your contributions will be licensed under its [MIT License](LICENSE).
