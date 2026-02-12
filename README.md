# AISS - AI Security Screener 🛡️

AISS is a comprehensive security screening tool designed specifically for AI agents, providing both self-assessment capabilities and external security testing.

## Features

### Self-Check Mode (For Agents)
- 🔍 Memory exposure scanning
- 🔑 API key storage audit
- 🧱 Boundary enforcement verification
- 📝 Security policy compliance

### External Testing Mode (For Users)
- 🔒 API security assessment
- 🎯 Prompt injection testing
- 🚫 Boundary bypass detection
- 🔐 Authentication testing

## Installation

```bash
pip install ai-security-screener
```

## Usage

### Self-Check Mode (For Agents)
```python
from aiss import AgentSelfCheck

checker = AgentSelfCheck()
results = checker.run_assessment()
print(results.report())
```

### External Testing (For Users)
```python
from aiss import SecurityScanner

scanner = SecurityScanner("https://your-agent.com")
results = scanner.run_scan()
print(results.generate_report())
```

## Security Best Practices

### API Key Handling
- Never hardcode API keys
- Use environment variables or secure vaults
- Example:
```python
import os

api_key = os.getenv('SERVICE_API_KEY')
if not api_key:
    raise SecurityError("API key not found in environment")
```

### Configuration
Create a `.env` file:
```bash
# .env
SERVICE_API_KEY=your_key_here
```

Add to .gitignore:
```bash
# .gitignore
.env
*.key
credentials/
```

## Testing

```bash
# Run test suite
pytest tests/

# Run security audit
aiss audit
```

## Development

### Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests
```bash
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/xyz`)
3. Commit changes (`git commit -am 'Add xyz feature'`)
4. Push branch (`git push origin feature/xyz`)
5. Create Pull Request

## Security

- Report security vulnerabilities to security@yourdomain.com
- Do not commit API keys or credentials
- Run `aiss audit` before commits
- Enable 2FA for repository access

## License

MIT License - see LICENSE file for details