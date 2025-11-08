# Contributing to HackerHardware.net

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive environment
- Report unacceptable behavior to the maintainers

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/fix
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/canstralian/hackerhardware-site.git
cd hackerhardware-site

# Set up Python environment
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests
pytest

# Start development server
uvicorn main:app --reload
```

## Code Standards

### Python Code

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small
- Maximum line length: 100 characters

Example:
```python
def calculate_threat_score(events: List[Dict]) -> float:
    """
    Calculate threat score based on security events.
    
    Args:
        events: List of security event dictionaries
        
    Returns:
        Threat score between 0.0 and 1.0
    """
    if not events:
        return 0.0
    
    # Implementation here
    return score
```

### JavaScript Code

- Use ES6+ features
- Follow Airbnb style guide
- Use meaningful variable names
- Add JSDoc comments for functions

### Documentation

- Update README.md if adding features
- Add inline comments for complex logic
- Update API documentation
- Include examples in documentation

## Testing

### Unit Tests

```bash
cd api
pytest tests/unit/
```

### Integration Tests

```bash
pytest tests/integration/
```

### Security Testing

```bash
bandit -r api/
```

## Pull Request Process

1. **Before submitting**:
   - Update documentation
   - Add/update tests
   - Run linters and fix issues
   - Ensure all tests pass
   - Rebase on main branch

2. **PR Description**:
   - Describe what changes you made
   - Explain why the changes are needed
   - Reference any related issues
   - Include screenshots for UI changes

3. **Review Process**:
   - Address reviewer feedback
   - Keep the PR focused and small
   - Be responsive to comments
   - Update the PR as needed

## Branch Naming

Use descriptive branch names:
- `feature/add-node-clustering`
- `fix/auth-token-expiry`
- `docs/update-deployment-guide`
- `refactor/simplify-threat-detection`

## Commit Messages

Write clear commit messages:

```
feat: add anomaly detection for edge nodes

- Implement ML-based anomaly detection
- Add threshold configuration
- Update documentation

Closes #123
```

Format: `<type>: <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## Security

### Reporting Vulnerabilities

- **DO NOT** create public issues for security vulnerabilities
- Email security@hackerhardware.net
- Include detailed reproduction steps
- Allow time for patching before disclosure

### Security Guidelines

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Validate all user inputs
- Use parameterized queries
- Keep dependencies updated

## Feature Requests

Have an idea? We'd love to hear it!

1. Check existing issues first
2. Create a detailed issue describing:
   - The problem it solves
   - Proposed solution
   - Alternative approaches
   - Impact on existing functionality

## Bug Reports

When reporting bugs:

1. Check if it's already reported
2. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - System information
   - Error messages/logs
   - Screenshots if applicable

## Documentation

Help improve documentation:

- Fix typos and grammar
- Add examples and tutorials
- Clarify unclear sections
- Update outdated information

## Community

- Join discussions in issues and PRs
- Help answer questions
- Share your use cases
- Contribute to documentation

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Recognized in project documentation

## Questions?

- Open an issue for general questions
- Check existing documentation
- Reach out to maintainers

Thank you for contributing to HackerHardware.net!
