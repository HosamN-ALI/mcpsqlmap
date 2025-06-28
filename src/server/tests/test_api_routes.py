import sys
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from server.api.routes import router
from server.core.mcp_server import MCPServer
from server.techniques.injection_handler import InjectionHandler, InjectionType
from server.bypass.waf_bypass import WAFBypass
from server.payloads.payload_manager import PayloadManager, PayloadSource
from server.integrations.integration_manager import IntegrationManager

@pytest.fixture
def client():
    """Create a test client"""
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@pytest.fixture
def mock_mcp_server():
    """Mock MCP server"""
    with patch('server.api.routes.mcp_server') as mock:
        mock.start_scan = AsyncMock(return_value={"status": "scanning"})
        yield mock

@pytest.fixture
def mock_injection_handler():
    """Mock injection handler"""
    with patch('server.api.routes.injection_handler') as mock:
        mock.execute_injection = AsyncMock(return_value={
            "success": True,
            "data": {"result": "test"}
        })
        mock.get_available_techniques = Mock(return_value=["blind", "union"])
        yield mock

@pytest.fixture
def mock_waf_bypass():
    """Mock WAF bypass"""
    with patch('server.api.routes.waf_bypass') as mock:
        mock.apply_technique = Mock(return_value={
            "success": True,
            "payload": "modified payload",
            "technique": "whitespace"
        })
        mock.apply_all_techniques = Mock(return_value=[{
            "success": True,
            "payload": "modified payload",
            "technique": "whitespace"
        }])
        mock.get_available_techniques = Mock(return_value=["whitespace", "case"])
        yield mock

@pytest.fixture
def mock_payload_manager():
    """Mock payload manager"""
    with patch('server.api.routes.payload_manager') as mock:
        mock.search_payloads = Mock(return_value=[
            {"content": "UNION SELECT", "category": "union"}
        ])
        mock.get_payloads = Mock(return_value=[
            {"content": "test payload", "category": "auth"}
        ])
        mock.add_custom_payload = Mock(return_value=True)
        yield mock

@pytest.fixture
def mock_integration_manager():
    """Mock integration manager"""
    with patch('server.api.routes.integration_manager') as mock:
        mock.analyze_with_deepseek = AsyncMock(return_value={
            "success": True,
            "data": {"analysis": "test result"}
        })
        mock.update_webui = AsyncMock(return_value={
            "success": True,
            "data": {"status": "updated"}
        })
        yield mock

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_start_scan(client, mock_mcp_server):
    """Test scan endpoint"""
    data = {
        "target_url": "http://example.com",
        "options": {"depth": 2}
    }
    
    response = client.post("/api/v1/scan", json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "scanning"}
    mock_mcp_server.start_scan.assert_called_once_with(
        data["target_url"],
        data["options"]
    )

@pytest.mark.asyncio
async def test_execute_injection(client, mock_injection_handler):
    """Test injection endpoint"""
    data = {
        "target": "http://example.com",
        "payload": "' OR '1'='1",
        "technique": "BLIND",
        "options": {}
    }
    
    mock_injection_handler.execute_injection.return_value = {
        "success": True,
        "data": {"result": "test"}
    }
    
    response = client.post("/api/v1/inject", json=data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response.get("success") is True
    assert "data" in json_response

def test_bypass_waf(client, mock_waf_bypass):
    """Test WAF bypass endpoint"""
    data = {
        "payload": "SELECT * FROM users",
        "techniques": ["whitespace", "case"]
    }
    
    mock_waf_bypass.apply_technique.side_effect = [
        {
            "success": True,
            "payload": "modified payload 1",
            "technique": "whitespace"
        },
        {
            "success": True,
            "payload": "modified payload 2",
            "technique": "case"
        }
    ]
    
    response = client.post("/api/v1/bypass", json=data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response.get("success") is True
    assert isinstance(json_response.get("results"), list)
    assert len(json_response.get("results")) == 2
    assert json_response.get("results")[0].get("payload") == "modified payload 1"
    assert json_response.get("results")[1].get("payload") == "modified payload 2"

def test_get_payloads(client, mock_payload_manager):
    """Test get payloads endpoint"""
    mock_payload_manager.get_payloads.return_value = [
        {"content": "test payload", "category": "auth"}
    ]
    
    response = client.get("/api/v1/payloads?source=fuzzdb&category=auth")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["content"] == "test payload"
    mock_payload_manager.get_payloads.assert_called_once_with(
        source="fuzzdb",
        category="auth"
    )

def test_search_payloads(client, mock_payload_manager):
    """Test payload search endpoint"""
    mock_payload_manager.search_payloads.return_value = [
        {"content": "UNION SELECT", "category": "union"}
    ]
    
    response = client.get("/api/v1/payloads?query=union")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["content"] == "UNION SELECT"
    mock_payload_manager.search_payloads.assert_called_once_with("union")

def test_add_custom_payload(client, mock_payload_manager):
    """Test add custom payload endpoint"""
    data = {
        "content": "' OR '1'='1",
        "category": "auth_bypass",
        "description": "Basic auth bypass"
    }
    
    response = client.post("/api/v1/payloads/custom", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Custom payload added successfully"}
    mock_payload_manager.add_custom_payload.assert_called_once_with(
        content=data["content"],
        category=data["category"],
        description=data["description"]
    )

@pytest.mark.asyncio
async def test_analyze_data(client, mock_integration_manager):
    """Test data analysis endpoint"""
    data = {
        "integration_type": "deepseek",
        "data": {"query": "SELECT * FROM users"}
    }
    
    from server.integrations.integration_manager import IntegrationResult
    mock_integration_manager.analyze_with_deepseek.return_value = IntegrationResult(
        success=True,
        data={"analysis": "test result"}
    )
    
    response = client.post("/api/v1/analyze", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"analysis": "test result"}
    }

def test_get_injection_techniques(client, mock_injection_handler):
    """Test get injection techniques endpoint"""
    response = client.get("/api/v1/techniques/injection")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "blind" in response.json()
    assert "union" in response.json()

def test_get_bypass_techniques(client, mock_waf_bypass):
    """Test get bypass techniques endpoint"""
    response = client.get("/api/v1/techniques/bypass")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "whitespace" in response.json()
    assert "case" in response.json()

def test_get_payload_sources(client):
    """Test get payload sources endpoint"""
    response = client.get("/api/v1/sources/payload")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(source in response.json() for source in [s.value for s in PayloadSource])

def test_invalid_injection_technique(client, mock_injection_handler):
    """Test invalid injection technique handling"""
    data = {
        "target": "http://example.com",
        "payload": "test",
        "technique": "INVALID",
        "options": {}
    }
    
    response = client.post("/api/v1/inject", json=data)
    assert response.status_code == 400
    assert "Invalid injection technique" in response.json()["detail"]

def test_failed_waf_bypass(client, mock_waf_bypass):
    """Test failed WAF bypass handling"""
    mock_waf_bypass.apply_all_techniques.return_value = []
    
    data = {
        "payload": "SELECT * FROM users",
        "techniques": []
    }
    
    response = client.post("/api/v1/bypass", json=data)
    assert response.status_code == 400
    assert "No bypass techniques were successful" in response.json()["detail"]

def test_failed_custom_payload(client, mock_payload_manager):
    """Test failed custom payload handling"""
    mock_payload_manager.add_custom_payload.return_value = False
    
    data = {
        "content": "test",
        "category": "test"
    }
    
    response = client.post("/api/v1/payloads/custom", json=data)
    assert response.status_code == 400
    assert "Failed to add custom payload" in response.json()["detail"]
