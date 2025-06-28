import pytest
import logging
from unittest.mock import Mock, patch, AsyncMock
from ..core.mcp_server import MCPServer

@pytest.fixture
def mcp_server():
    return MCPServer()

def test_server_initialization(mcp_server):
    """Test MCP server initialization"""
    assert mcp_server.app is not None
    assert mcp_server.logger is not None

@pytest.mark.asyncio
async def test_start_scan_valid_url(mcp_server):
    """Test starting a scan with valid URL"""
    target_url = "http://example.com"
    options = {"technique": "B", "threads": 5}
    
    with patch('subprocess.Popen') as mock_popen:
        # Mock the subprocess.Popen
        mock_process = Mock()
        mock_process.communicate.return_value = ("SQLMap output", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        result = await mcp_server.start_scan(target_url, options)
        
        assert result["status"] == "scan_started"
        assert result["target"] == target_url
        assert result["options"] == options
        assert result["sqlmap_result"]["status"] == "success"
        
        # Verify SQLMap command
        mock_popen.assert_called_once()
        cmd_args = mock_popen.call_args[0][0]
        assert cmd_args[0] == "sqlmap"
        assert cmd_args[1] == "-u"
        assert cmd_args[2] == target_url

@pytest.mark.asyncio
async def test_start_scan_invalid_url(mcp_server):
    """Test starting a scan with invalid URL"""
    target_url = "invalid-url"
    options = {}
    
    with pytest.raises(Exception) as exc_info:
        await mcp_server.start_scan(target_url, options)
    
    assert "Invalid URL format" in str(exc_info.value)

@pytest.mark.asyncio
async def test_start_scan_sqlmap_error(mcp_server):
    """Test handling SQLMap execution error"""
    target_url = "http://example.com"
    options = {}
    
    with patch('subprocess.Popen') as mock_popen:
        # Mock SQLMap failure
        mock_process = Mock()
        mock_process.communicate.return_value = ("", "SQLMap error")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        with pytest.raises(Exception) as exc_info:
            await mcp_server.start_scan(target_url, options)
        
        assert "SQLMap execution failed" in str(exc_info.value)

@pytest.mark.asyncio
async def test_deepseek_analysis_success(mcp_server):
    """Test successful Deepseek API analysis"""
    query = "SELECT * FROM users WHERE id = 1"
    api_key = "sk-1bd5de3f31db429cb8cbe73875537c5c"
    
    mock_response = {
        "choices": [{
            "message": {
                "content": "Analysis of SQL query..."
            }
        }]
    }
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value.status = 200
        mock_context.__aenter__.return_value.json = AsyncMock(
            return_value=mock_response
        )
        mock_post.return_value = mock_context
        
        result = await mcp_server.analyze_with_deepseek(query, api_key)
        
        assert result == mock_response
        mock_post.assert_called_once()
        
        # Verify API call
        call_kwargs = mock_post.call_args[1]
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["Authorization"] == f"Bearer {api_key}"

@pytest.mark.asyncio
async def test_deepseek_analysis_error(mcp_server):
    """Test Deepseek API error handling"""
    query = "SELECT * FROM users"
    api_key = "invalid-key"
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value.status = 401
        mock_context.__aenter__.return_value.text = AsyncMock(
            return_value="Invalid API key"
        )
        mock_post.return_value = mock_context
        
        with pytest.raises(Exception) as exc_info:
            await mcp_server.analyze_with_deepseek(query, api_key)
        
        assert "Deepseek API error" in str(exc_info.value)

def test_execute_sqlmap_command(mcp_server):
    """Test SQLMap command execution"""
    target_url = "http://example.com"
    options = {
        "technique": "BEUSTQ",
        "threads": 5,
        "batch": True,
        "random-agent": True
    }
    
    with patch('subprocess.Popen') as mock_popen:
        mock_process = Mock()
        mock_process.communicate.return_value = ("SQLMap output", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        result = mcp_server._execute_sqlmap_command(target_url, options)
        
        assert result["status"] == "success"
        assert "SQLMap output" in result["output"]
        
        # Verify command construction
        cmd = result["command"].split()
        assert "sqlmap" in cmd
        assert "-u" in cmd
        assert target_url in cmd
        assert "--technique" in cmd
        assert "--threads" in cmd
        assert "--batch" in cmd
        assert "--random-agent" in cmd

def test_logger_setup(mcp_server):
    """Test logger configuration"""
    logger = mcp_server._setup_logger()

    assert logger.name == "mcp_server"
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)
