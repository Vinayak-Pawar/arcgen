# Contributing to Arcgen

First off, thank you for considering contributing to Arcgen! It's people like you that make Arcgen such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by a spirit of respect and collaboration. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**.
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** if possible.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to most Arcgen users.

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python and TypeScript style guides
* Include thoughtful comments in your code
* End all files with a newline
* Avoid platform-dependent code

## Development Process

1. **Fork the repo** and create your branch from `main`.
2. **Install dependencies:**
   - Backend: `cd backend && pip install -r requirements.txt`
   - Frontend: `cd frontend && npm install`
3. **Make your changes:**
   - Write clear, commented code
   - Follow existing code style
   - Test your changes thoroughly
4. **Commit your changes:**
   - Use clear and meaningful commit messages
   - Follow conventional commits format if possible
5. **Push to your fork** and submit a pull request

## Style Guides

### Python Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use meaningful variable and function names
* Add docstrings to functions and classes
* Keep functions focused and small
* Use type hints where appropriate

Example:
```python
def generate_diagram(prompt: str) -> dict:
    """
    Generate a diagram from a natural language prompt.
    
    Args:
        prompt: The natural language description of the system
        
    Returns:
        A dictionary containing the generated CSV data
    """
    # Implementation here
    pass
```

### TypeScript Style Guide

* Follow the project's ESLint configuration
* Use TypeScript interfaces for props
* Use meaningful variable and function names
* Keep components focused and reusable
* Use functional components with hooks

Example:
```typescript
interface ChatPanelProps {
    onSendMessage: (message: string) => Promise<void>;
    messages: Message[];
    isLoading: boolean;
}

export default function ChatPanel({ onSendMessage, messages, isLoading }: ChatPanelProps) {
    // Component implementation
}
```

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Project Structure

```
arcgen/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application file
│   └── requirements.txt
├── frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/     # Next.js app directory
│   │   └── components/  # React components
│   └── package.json
├── archive/          # Previous implementation attempts
└── README.md
```

## Testing

Currently, the project is in early development. As it matures, we will add:
- Unit tests for backend endpoints
- Integration tests for the full flow
- E2E tests for the frontend

If you're adding new features, please consider adding tests.

## Documentation

* Update the README.md if you change functionality
* Add JSDoc/docstring comments to new functions
* Update API documentation if you add/modify endpoints

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## Recognition

Contributors will be recognized in the README.md file. Thank you for your contributions!

---

**Remember:** The goal of Arcgen is to make system design accessible to everyone. Keep this in mind when contributing, and let's build something amazing together! 🚀

