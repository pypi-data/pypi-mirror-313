# Contributing to func

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/genfunc.git
cd func
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Development Process

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Run tests:
```bash
pytest
```

4. Update documentation if needed
5. Commit your changes:
```bash
git add .
git commit -m "Add your feature description"
```

6. Push to your fork:
```bash
git push origin feature/your-feature-name
```

7. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Include type hints
- Keep functions focused and single-purpose

## Testing

1. Write tests for new features:
```python
def test_your_feature():
    # Test code here
    assert expected == actual
```

2. Run tests with coverage:
```bash
pytest --cov=func tests/
```

3. Ensure test coverage remains high

## Documentation

1. Update relevant documentation
2. Add docstrings to new code
3. Include examples where appropriate
4. Update CHANGELOG.md

## Pull Request Process

1. Update README.md if needed
2. Update version numbers
3. Update CHANGELOG.md
4. Ensure all tests pass
5. Wait for review

## Code of Conduct

1. Be respectful and inclusive
2. Provide constructive feedback
3. Focus on what is best for the community
4. Show empathy towards others

## Questions?

- Open an issue for discussion
- Join our community chat
- Contact maintainers directly

Thank you for contributing to func!