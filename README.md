# Advanced MCP SQLMap Server

An advanced Model Context Protocol (MCP) server for vulnerability discovery using SQLMap with full integration capabilities. This server provides a comprehensive suite of SQL injection testing tools, WAF bypass techniques, and integration with LangChain and Open WebUI.

## Features

- **Advanced SQL Injection Techniques**
  - Blind SQL Injection (Time-based and Boolean-based)
  - UNION-based Injection
  - Stacked Queries
  - Stored Procedure Injection
  - Out-of-Band (OOB) Exploitation
  - NoSQL Injection Support

- **WAF Bypass Capabilities**
  - Whitespace Manipulation
  - Case Randomization
  - Comment Injection
  - URL Encoding
  - Hex Encoding
  - Unicode Encoding
  - String Concatenation
  - Character Encoding
  - SQL Wildcard Techniques

- **Comprehensive Payload Management**
  - Integration with FuzzDB
  - PayloadsAllTheThings Collection
  - NoSQL Injection Wordlists
  - Custom Payload Support
  - Advanced Payload Search and Filtering

- **AI-Powered Analysis**
  - LangChain Integration for Intelligent Analysis
  - Automated Vulnerability Assessment
  - Smart Payload Generation
  - WAF Bypass Strategy Recommendation

- **Real-time Monitoring**
  - Integration with Open WebUI
  - Live Scan Progress Updates
  - Real-time Result Analysis
  - Interactive Dashboard

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/advanced-mcp-sqlmap-server.git
cd advanced-mcp-sqlmap-server
```

2. Create and activate a virtual environment:
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
# Create .env file
cp .env.example .env

# Edit .env file with your configuration
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the server:
```bash
python -m src.server.main
```

2. The server will be available at `http://localhost:8000`

3. API Documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Core Endpoints

- `POST /api/v1/scan` - Start a new vulnerability scan
- `POST /api/v1/inject` - Execute SQL injection attack
- `POST /api/v1/bypass` - Apply WAF bypass techniques
- `GET /api/v1/payloads` - Get injection payloads
- `POST /api/v1/analyze` - Analyze data using AI integration

### Management Endpoints

- `GET /api/v1/techniques/injection` - List available injection techniques
- `GET /api/v1/techniques/bypass` - List available WAF bypass techniques
- `GET /api/v1/sources/payload` - List available payload sources
- `GET /api/v1/health` - Check server health status

## Integration Examples

### Starting a Scan

```python
import requests

scan_data = {
    "target_url": "http://example.com/vulnerable.php",
    "options": {
        "technique": "blind",
        "delay": 1,
        "threads": 5
    }
}

response = requests.post(
    "http://localhost:8000/api/v1/scan",
    json=scan_data
)
print(response.json())
```

### Executing Injection

```python
injection_data = {
    "target": "http://example.com/login",
    "payload": "' OR '1'='1",
    "technique": "union",
    "options": {
        "columns": 3,
        "dbms": "mysql"
    }
}

response = requests.post(
    "http://localhost:8000/api/v1/inject",
    json=injection_data
)
print(response.json())
```

## Security Considerations

1. This tool is for educational and authorized testing purposes only
2. Always obtain proper authorization before testing
3. Use in controlled environments only
4. Follow responsible disclosure practices
5. Comply with all applicable laws and regulations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- SQLMap Project
- FuzzDB Project
- PayloadsAllTheThings
- LangChain
- FastAPI

## Disclaimer

This tool is for educational purposes only. Users are responsible for obtaining proper authorization before conducting any security testing. The authors are not responsible for any misuse or damage caused by this tool.
