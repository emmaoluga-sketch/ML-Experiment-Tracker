# Contributing to ML Experiment Tracker

We welcome contributions to the ML Experiment Tracker project! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/ml-experiment-tracker.git
cd ml-experiment-tracker

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

## Development Workflow

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for new functionality
4. Ensure all tests pass
5. Commit your changes with clear messages
6. Push to your fork
7. Submit a pull request

## Code Style

### Python

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Format code with Black: `black .`
- Lint with flake8: `flake8 .`

### JavaScript/React

- Use ESLint
- Use Prettier for formatting
- Write meaningful component names
- Include JSDoc comments for complex logic

## Commit Messages

Use clear, descriptive commit messages:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for test additions/changes

Example: `feat: Add export functionality for experiments`

## Pull Request Process

1. Update the README.md with any new features or changes
2. Update requirements.txt or package.json if dependencies change
3. Ensure all tests pass
4. Request review from maintainers
5. Address any feedback

## Reporting Issues

When reporting bugs, please include:

- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python/Node version, etc.)

## Feature Requests

We welcome feature requests! Please provide:

- Use case and motivation
- Proposed solution
- Alternative approaches considered

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
