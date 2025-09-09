# Contributing to Restaurant Social SaaS

Thank you for your interest in contributing to Restaurant Social SaaS! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. **Open a feature request** using the appropriate template
2. **Describe the use case** and why it would be valuable
3. **Consider the scope** - is this a core feature or plugin?
4. **Be open to discussion** about implementation approaches

### Code Contributions

#### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/restaurant-social-saas.git
   cd restaurant-social-saas
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

#### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Commit your changes** with clear messages:
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request** on GitHub

## 📝 Coding Standards

### Python Code Style

- **Follow PEP 8** for Python code formatting
- **Use meaningful variable names** that describe their purpose
- **Add docstrings** to all functions and classes:
  ```python
  def generate_caption(self, image_data: str) -> str:
      """Generate AI-powered caption for food image.
      
      Args:
          image_data: Base64 encoded image string
          
      Returns:
          Generated caption with hashtags
      """
  ```
- **Include type hints** where appropriate:
  ```python
  def process_restaurant_data(restaurant_id: int) -> Dict[str, Any]:
  ```

### Code Organization

- **Keep functions small** and focused on a single responsibility
- **Use classes** for related functionality
- **Separate concerns** - keep AI logic separate from web routes
- **Add comments** for complex business logic

### Testing

- **Write tests** for new functionality
- **Test edge cases** and error conditions
- **Include integration tests** for API endpoints
- **Test AI fallback scenarios** when OpenAI is unavailable

## 🏗 Project Structure

```
restaurant-social-saas/
├── src/                          # Main application code
│   ├── main.py                   # Flask application entry point
│   ├── enhanced_ai_captions_simple.py  # AI caption generation
│   └── static/                   # Static files (CSS, JS, images)
├── docs/                         # Documentation
│   ├── ai-setup-guide.md         # AI configuration guide
│   └── restaurant-social-ai-enhancement-report.md
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_ai_captions.py
```

### Writing Tests

1. **Test file naming**: `test_*.py` or `*_test.py`
2. **Test function naming**: `test_function_name_scenario()`
3. **Use fixtures** for common test data
4. **Mock external services** (OpenAI API calls)

Example test:
```python
def test_generate_caption_with_fallback():
    """Test caption generation when AI is unavailable."""
    generator = EnhancedAICaptionGenerator(api_key="")
    result = generator.generate_caption_from_image("fake_image_data")
    assert "🍽️" in result
    assert "#foodie" in result
```

## 🚀 AI Development Guidelines

### Working with AI Features

1. **Always provide fallbacks** for when AI services are unavailable
2. **Handle API errors gracefully** with try/catch blocks
3. **Implement rate limiting** to avoid API quota issues
4. **Test with and without** OpenAI API keys
5. **Consider cost implications** of AI feature usage

### AI Prompt Engineering

1. **Be specific** in prompts for consistent results
2. **Include context** about restaurants and food
3. **Test prompts thoroughly** with various image types
4. **Document prompt changes** and their effects

## 📚 Documentation

### Code Documentation

- **Document all public functions** with docstrings
- **Include usage examples** in docstrings
- **Update README.md** when adding new features
- **Add inline comments** for complex logic

### User Documentation

- **Update setup guides** when changing requirements
- **Include screenshots** for UI changes
- **Write clear instructions** for new features
- **Test documentation** by following it step-by-step

## 🔍 Review Process

### Pull Request Guidelines

1. **Fill out the PR template** completely
2. **Link related issues** using keywords (fixes #123)
3. **Provide clear description** of changes
4. **Include screenshots** for UI changes
5. **Ensure tests pass** before requesting review

### Review Criteria

- **Code quality** and adherence to standards
- **Test coverage** for new functionality
- **Documentation** updates where needed
- **Performance** impact consideration
- **Security** implications review

## 🌟 Recognition

Contributors will be recognized in:
- **README.md** acknowledgments section
- **Release notes** for significant contributions
- **GitHub contributors** page

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: For sensitive issues or private communication

### Development Questions

- **Check existing documentation** first
- **Search closed issues** for similar problems
- **Ask specific questions** with context and examples
- **Be patient** - maintainers are volunteers

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- **Test coverage** improvements
- **Documentation** enhancements
- **Performance** optimizations
- **Mobile UI** improvements

### Medium Priority
- **New AI features** (video captions, multi-language)
- **Additional social platforms** integration
- **Analytics** and reporting features
- **Accessibility** improvements

### Low Priority
- **Code refactoring** for maintainability
- **Developer tools** and automation
- **Example applications** and tutorials

## 📋 Checklist for Contributors

Before submitting a pull request:

- [ ] Code follows project style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Changes are tested locally
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] Related issues are linked

## 🙏 Thank You

Your contributions help make Restaurant Social SaaS better for restaurant owners worldwide. Every contribution, no matter how small, is valuable and appreciated!

---

*Happy coding! 🚀*

