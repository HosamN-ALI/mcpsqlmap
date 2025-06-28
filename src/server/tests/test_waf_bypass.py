import pytest
from unittest.mock import patch, AsyncMock
from ..bypass.waf_bypass import WAFBypass, BypassResult

@pytest.fixture
def waf_bypass():
    return WAFBypass()

def test_whitespace_bypass(waf_bypass):
    """Test whitespace manipulation bypass technique"""
    payload = "SELECT * FROM users"
    result = waf_bypass.apply_whitespace_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "whitespace"
    assert " " not in result.payload  # Should replace spaces

def test_case_bypass(waf_bypass):
    """Test case manipulation bypass technique"""
    payload = "SELECT * FROM users WHERE id = 1"
    result = waf_bypass.apply_case_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "case"
    assert result.payload != payload  # Should have different case
    assert result.payload.lower() == payload.lower()  # Same when lowercased

def test_comments_bypass(waf_bypass):
    """Test SQL comment injection bypass technique"""
    payload = "SELECT * FROM users"
    result = waf_bypass.apply_comments_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "comments"
    assert "/*" in result.payload or "--" in result.payload or "#" in result.payload

def test_url_encode_bypass(waf_bypass):
    """Test URL encoding bypass technique"""
    payload = "SELECT * FROM users WHERE name = 'admin'"
    result = waf_bypass.apply_url_encode_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "url_encode"
    assert "%" in result.payload  # Should contain URL encoded characters

def test_hex_encode_bypass(waf_bypass):
    """Test hexadecimal encoding bypass technique"""
    payload = "SELECT * FROM users"
    result = waf_bypass.apply_hex_encode_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "hex_encode"
    assert result.payload.startswith("0x")  # Should be hex encoded

def test_concat_bypass(waf_bypass):
    """Test string concatenation bypass technique"""
    payload = "SELECT * FROM users"
    result = waf_bypass.apply_concat_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "concat"
    assert "CONCAT" in result.payload

def test_char_encode_bypass(waf_bypass):
    """Test CHAR() encoding bypass technique"""
    payload = "SELECT * FROM users"
    result = waf_bypass.apply_char_encode_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert result.technique == "char_encode"
    assert result.payload.startswith("CHAR(")

def test_multiple_techniques(waf_bypass):
    """Test applying multiple bypass techniques"""
    payload = "SELECT * FROM users WHERE id = 1"
    results = waf_bypass.apply_all_techniques(payload)
    
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results:
        assert isinstance(result, BypassResult)
        assert result.success is True
        assert result.payload is not None
        assert result.technique is not None

def test_invalid_technique(waf_bypass):
    """Test handling of invalid bypass technique"""
    payload = "SELECT * FROM users"
    result = waf_bypass.apply_technique("invalid_technique", payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is False
    assert result.error is not None

def test_empty_payload(waf_bypass):
    """Test handling of empty payload"""
    payload = ""
    result = waf_bypass.apply_whitespace_bypass(payload)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload == ""

@pytest.mark.asyncio
async def test_deepseek_analysis(waf_bypass):
    """Test Deepseek integration for bypass analysis"""
    payload = "SELECT * FROM users"

    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value.status = 200
        mock_context.__aenter__.return_value.json = AsyncMock(
            return_value={
                "analysis": {
                    "bypass_effectiveness": "high",
                    "suggested_techniques": ["comments", "hex_encode"]
                }
            }
        )
        mock_post.return_value = mock_context
        
        result = await waf_bypass.analyze_with_deepseek(
            payload,
            "sk-1bd5de3f31db429cb8cbe73875537c5c"
        )
        
        assert result is not None
        assert "bypass_effectiveness" in result["analysis"]
        assert "suggested_techniques" in result["analysis"]

def test_generate_tampered_payload(waf_bypass):
    """Test generating tampered payload with multiple techniques"""
    payload = "SELECT * FROM users WHERE id = 1"
    techniques = ["case", "comments", "hex_encode"]
    
    result = waf_bypass.generate_tampered_payload(payload, techniques)
    
    assert isinstance(result, BypassResult)
    assert result.success is True
    assert result.payload is not None
    assert all(tech in result.technique for tech in techniques)

def test_available_techniques(waf_bypass):
    """Test getting available bypass techniques"""
    techniques = waf_bypass.get_available_techniques()
    
    assert isinstance(techniques, list)
    assert len(techniques) > 0
    expected_techniques = [
        "whitespace", "case", "comments", "url_encode",
        "hex_encode", "concat", "char_encode"
    ]
    assert all(tech in techniques for tech in expected_techniques)
