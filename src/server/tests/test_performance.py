import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from server.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_concurrent_scan_requests():
    """Simulate concurrent scan requests to test performance and load handling"""
    with patch('server.api.routes.mcp_server') as mock_server:
        mock_server.start_scan = AsyncMock(return_value={"status": "scanning"})
        
        async def send_scan_request():
            data = {
                "target_url": "http://example.com",
                "options": {"depth": 1}
            }
            response = client.post("/api/v1/scan", json=data)
            assert response.status_code == 200
            assert response.json().get("status") == "scanning"

        tasks = [send_scan_request() for _ in range(20)]  # Simulate 20 concurrent requests
        await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_concurrent_injection_requests():
    """Simulate concurrent injection requests"""
    with patch('server.api.routes.injection_handler') as mock_handler:
        mock_handler.execute_injection = AsyncMock(return_value={
            "success": True,
            "data": {"result": "test"}
        })
        
        async def send_injection_request():
            data = {
                "target": "http://example.com",
                "payload": "' OR '1'='1",
                "technique": "BLIND",
                "options": {}
            }
            response = client.post("/api/v1/inject", json=data)
            assert response.status_code == 200
            assert response.json().get("success") is True

        tasks = [send_injection_request() for _ in range(20)]
        await asyncio.gather(*tasks)
