import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
import os
import uvicorn

from server.main import app, start_server, lifespan

@pytest.fixture
def test_client():
    """Fixture for FastAPI test client"""
    return TestClient(app)

@pytest.mark.asyncio
async def test_lifespan():
    """Test lifespan context manager"""
    mock_app = MagicMock()
    
    with patch('server.main.IntegrationManager') as mock_manager:
        mock_instance = AsyncMock()
        mock_manager.return_value = mock_instance
        
        async with lifespan(mock_app):
            mock_manager.assert_called_once()
            mock_instance.initialize.assert_awaited_once()
        
        mock_instance.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_lifespan_error():
    """Test lifespan error handling"""
    mock_app = MagicMock()
    
    with patch('server.main.IntegrationManager') as mock_manager:
        mock_instance = MagicMock()
        mock_instance.initialize.side_effect = Exception("Init error")
        mock_manager.return_value = mock_instance
        
        with pytest.raises(Exception, match="Init error"):
            async with lifespan(mock_app):
                pass

def test_root_endpoint(test_client):
    """Test root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"

def test_status_endpoint(test_client):
    """Test status endpoint"""
    response = test_client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "integrations" in data
    assert isinstance(data["integrations"], dict)

def test_status_endpoint_error(test_client):
    """Test status endpoint error handling"""
    with patch.dict(os.environ, {"SIMULATE_STATUS_ERROR": "true"}):
        response = test_client.get("/status")
        assert response.status_code == 500
        assert "detail" in response.json()

def test_start_server():
    """Test server startup function"""
    mock_config = {"key": "value"}
    
    with patch('uvicorn.run') as mock_run:
        start_server(
            host="localhost",
            port=8000,
            reload=True,
            config=mock_config
        )
        
        mock_run.assert_called_once_with(
            "server.main:app",
            host="localhost",
            port=8000,
            reload=True,
            log_level="info"
        )

def test_start_server_error():
    """Test server startup error handling"""
    with patch('uvicorn.run', side_effect=Exception("Startup error")):
        with pytest.raises(Exception, match="Failed to start server"):
            start_server()

def test_environment_variables():
    """Test environment variable handling"""
    with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}):
        with patch('uvicorn.run'):
            start_server()
            # No warning should be logged

    with patch.dict(os.environ, clear=True):
        with patch('uvicorn.run'),              patch('server.main.logger.warning') as mock_warning:
            start_server()
            mock_warning.assert_called_once_with(
                "DEEPSEEK_API_KEY not found in environment variables"
            )

@pytest.mark.asyncio
async def test_lifespan_startup():
    """Test lifespan startup handling"""
    mock_app = MagicMock()
    
    with patch('server.main.IntegrationManager') as mock_manager:
        mock_instance = AsyncMock()
        mock_manager.return_value = mock_instance
        
        async with lifespan(mock_app):
            # Check initialization
            mock_manager.assert_called_once()
            mock_instance.initialize.assert_awaited_once()
            
            # Verify global instance is set
            from server.main import integration_manager
            assert integration_manager is not None

@pytest.mark.asyncio
async def test_lifespan_startup_error():
    """Test lifespan startup error handling"""
    mock_app = MagicMock()
    
    with patch('server.main.IntegrationManager') as mock_manager:
        mock_instance = AsyncMock()
        mock_instance.initialize.side_effect = Exception("Init error")
        mock_manager.return_value = mock_instance
        
        with pytest.raises(Exception, match="Init error"):
            async with lifespan(mock_app):
                pass

@pytest.mark.asyncio
async def test_lifespan_shutdown():
    """Test lifespan shutdown handling"""
    mock_app = MagicMock()
    
    with patch('server.main.IntegrationManager') as mock_manager:
        mock_instance = AsyncMock()
        mock_manager.return_value = mock_instance
        
        async with lifespan(mock_app):
            pass
        
        # Verify cleanup
        mock_instance.close.assert_awaited_once()
        
        # Verify global instance is cleaned up
        from server.main import integration_manager
        assert integration_manager is None
