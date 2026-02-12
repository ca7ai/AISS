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

### Enhanced Reporting 📊
- Multiple output formats (text, JSON, HTML)
- Interactive visualizations
- Severity distribution charts
- Findings timeline
- Custom branding support
- Detailed proof and remediation
- Executive summaries

### Configuration Options ⚙️
- Customizable scan parameters
- Report customization
- Company branding
- Output paths
- Test thresholds
- Custom user agents

## Installation

```bash
pip install ai-security-screener
```

## Configuration

Create a config file at `~/.config/aiss/config.yml`:

```yaml
scan:
  max_requests: 50
  timeout: 30
  user_agent: "AISS-Scanner/1.0"
  follow_redirects: true
  verify_ssl: true

report:
  detail_level: "standard"  # minimal, standard, detailed
  include_proof: true
  output_format: "html"     # text, json, html
  save_path: "~/aiss-reports"
  company_name: "Your Company"
  logo_path: "~/company-logo.png"

log_level: "INFO"
```

Or configure via environment variables:
```bash
export AISS_CONFIG=/path/to/config.yml
export AISS_LOG_LEVEL=DEBUG
export AISS_REPORT_FORMAT=html
```

## Usage

### Command Line Interface
```bash
# Run scan with default config
aiss scan https://agent-url.com

# Specify output format
aiss scan https://agent-url.com --format html

# Save report
aiss scan https://agent-url.com -o report.html

# Run self-check
aiss self-check
```

### Python API
```python
from aiss import SecurityScanner, AISSConfig

# Load custom config
config = AISSConfig.load("my-config.yml")

# Initialize scanner
scanner = SecurityScanner("https://agent-url.com", config)

# Run scan
results = scanner.run_scan()

# Generate report
report = scanner.generate_report(results)
```

### Report Customization
```python
from aiss.reporting import ReportGenerator
from aiss.core.config import ReportConfig

# Configure reporting
config = ReportConfig(
    detail_level="detailed",
    output_format="html",
    company_name="Your Company",
    logo_path="path/to/logo.png"
)

# Generate custom report
generator = ReportGenerator(config)
report = generator.generate(findings, metadata)
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

### Configuration Security
- Keep config files secure
- Don't commit sensitive configs
- Use environment variables for secrets
- Validate SSL certificates
- Set appropriate timeouts

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
pytest tests/ -v --cov=aiss
```

### Building Reports
```bash
# Install reporting dependencies
pip install aiss[reporting]

# Generate all report formats
aiss scan https://agent-url.com --format all
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

