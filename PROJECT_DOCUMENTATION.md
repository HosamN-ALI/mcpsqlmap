# Project Documentation for Advanced MCP SQLMap Server

---

## Overview

This project is an advanced Model Context Protocol (MCP) server designed for vulnerability discovery using SQLMap. It includes backend APIs, middleware, and frontend components to facilitate security testing, payload management, and integration with external analysis services.

---

## Project Structure

```
/project/sandbox/user-workspace/
├── src/
│   ├── app/                      # Frontend React components and pages
│   ├── components/               # UI components
│   ├── hooks/                    # React hooks
│   ├── lib/                      # Utility functions
│   ├── mcp_server.egg-info/      # Python package metadata
│   ├── server/                   # Backend server code
│   │   ├── api/                  # API route handlers
│   │   ├── bypass/               # WAF bypass techniques
│   │   ├── core/                 # Core server logic
│   │   ├── integrations/         # External service integrations (Deepseek, OpenWebUI)
│   │   ├── payloads/             # Payload management (loading, searching, adding)
│   │   ├── techniques/           # Injection and attack techniques
│   │   ├── tests/                # Unit and integration tests
│   │   ├── main.py               # FastAPI app entry point and lifecycle management
│   │   └── api/routes.py         # API route definitions
│   ├── tests/                   # Additional test files
│   └── ...                      # Other project files
├── PayloadsAllTheThings-master/  # Local payload repository for PayloadsAllTheThings
├── fuzzdb-master/                # Local payload repository for FuzzDB
├── nosqlinjection_wordlists-master/ # Local payload repository for NoSQL injection payloads
├── README.md                    # Project readme
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Python project config
├── package.json                 # Node.js dependencies
└── ...                         # Other config and resource files
```

---

## Backend

- **Framework:** FastAPI
- **Main entry:** `src/server/main.py`
- **API Routes:** Defined in `src/server/api/routes.py`
- **Payload Management:**  
  - `src/server/payloads/payload_manager.py` handles loading payloads from local directories (`PayloadsAllTheThings`, `FuzzDB`, `NoSQL`), searching, adding custom payloads, and saving them.
  - Payload sources are configured to load from local paths for offline and fast access.
- **Integrations:**  
  - `src/server/integrations/integration_manager.py` manages external services like Deepseek and OpenWebUI.
- **WAF Bypass:**  
  - `src/server/bypass/waf_bypass.py` contains logic for bypassing Web Application Firewalls.
- **Injection Techniques:**  
  - `src/server/techniques/injection_handler.py` implements various injection techniques.
- **Core Server Logic:**  
  - `src/server/core/mcp_server.py` manages scanning and server lifecycle.

---

## Frontend

- Located in `src/app/` and `src/components/`
- Built with React and Tailwind CSS
- Provides UI components for scanning, payload management, and results display

---

## Middleware and Logic

- Middleware includes CORS handling and request validation
- Business logic is split across modules for injection, payload management, and integrations
- Async programming with `asyncio` and `aiohttp` for network calls and file I/O

---

## Payload Sources

- **PayloadsAllTheThings:** Loaded from local path `/project/sandbox/user-workspace/PayloadsAllTheThings-master`
- **FuzzDB:** Loaded from local path `/project/sandbox/user-workspace/fuzzdb-master/attack/sql-injection`
- **NoSQL Injection:** Loaded from local path `/project/sandbox/user-workspace/nosqlinjection_wordlists-master`

Payloads are loaded recursively from these directories, categorized by their relative folder paths.

---

## Testing

- Tests are located in `src/server/tests/`
- Use `pytest` with `pytest-asyncio` for async tests
- Coverage includes unit and integration tests for payload loading, injection handling, API routes, and integrations
- Tests mock external services and file I/O for reliability

---

## How to Run

1. Install dependencies:
   - Python packages from `requirements.txt` or `pyproject.toml`
   - Node.js packages from `package.json`
2. Ensure local payload repositories are present in the workspace:
   - `PayloadsAllTheThings-master`
   - `fuzzdb-master`
   - `nosqlinjection_wordlists-master`
3. Run backend server:
   ```bash
   python -m src.server.main
   ```
4. Run frontend development server (if applicable):
   ```bash
   npm run dev
   ```
5. Run tests:
   ```bash
   python -m pytest src/server/tests
   ```

---

## Notes

- The project uses local payload repositories for offline and fast access.
- Async initialization is used for payload loading and integrations.
- Logging is configured for detailed error and info messages.
- FastAPI lifespan events manage startup and shutdown lifecycle.

---

## Contact and Contribution

- See `CONTRIBUTING.md` in the root and payload repositories for contribution guidelines.
- For issues, refer to `PROJECT_ISSUES_AND_FIXES.md`.

---

This documentation provides a comprehensive overview of the project for new developers or auditors to understand the architecture, components, and usage.
