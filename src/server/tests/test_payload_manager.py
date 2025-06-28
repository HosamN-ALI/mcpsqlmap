import pytest
import json
import os
from unittest.mock import Mock, patch
from ..payloads.payload_manager import PayloadManager, PayloadSource, Payload

@pytest.fixture
def payload_manager():
    return PayloadManager()

@pytest.fixture
def mock_response():
    class MockResponse:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text
            
        def json(self):
            return json.loads(self.text)
    return MockResponse

def test_initialization(payload_manager):
    """Test PayloadManager initialization"""
    assert isinstance(payload_manager.payloads, dict)
    for source in PayloadSource:
        assert source.value in payload_manager.payloads

@pytest.mark.asyncio
async def test_load_fuzzdb_payloads(payload_manager, mock_response):
    """Test loading payloads from FuzzDB"""
    mock_payloads = """
    ' OR '1'='1
    ' UNION SELECT NULL--
    1'; DROP TABLE users--
    """
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response(200, mock_payloads)
        await payload_manager._load_fuzzdb_payloads()
        
        assert len(payload_manager.payloads[PayloadSource.FUZZDB.value]) > 0
        payload = payload_manager.payloads[PayloadSource.FUZZDB.value][0]
        assert isinstance(payload, Payload)
        assert payload.source == PayloadSource.FUZZDB.value

@pytest.mark.asyncio
async def test_load_pat_payloads(payload_manager, mock_response):
    """Test loading payloads from PayloadsAllTheThings"""
    mock_payloads = """
    admin' --
    admin' #
    admin'/*
    """
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response(200, mock_payloads)
        await payload_manager._load_pat_payloads()
        
        assert len(payload_manager.payloads[PayloadSource.PAYLOADSALLTHETHINGS.value]) > 0
        payload = payload_manager.payloads[PayloadSource.PAYLOADSALLTHETHINGS.value][0]
        assert isinstance(payload, Payload)
        assert payload.source == PayloadSource.PAYLOADSALLTHETHINGS.value

@pytest.mark.asyncio
async def test_load_nosql_payloads(payload_manager, mock_response):
    """Test loading NoSQL payloads"""
    mock_payloads = """
    {"$ne": null}
    {"$gt": ""}
    {"$where": "this.password.length > 0"}
    """
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response(200, mock_payloads)
        await payload_manager._load_nosql_payloads()
        
        assert len(payload_manager.payloads[PayloadSource.NOSQL.value]) > 0
        payload = payload_manager.payloads[PayloadSource.NOSQL.value][0]
        assert isinstance(payload, Payload)
        assert payload.source == PayloadSource.NOSQL.value

def test_add_custom_payload(payload_manager):
    """Test adding custom payload"""
    content = "' OR 'custom'='custom"
    category = "authentication_bypass"
    description = "Custom authentication bypass payload"
    
    success = payload_manager.add_custom_payload(
        content=content,
        category=category,
        description=description
    )
    
    assert success is True
    custom_payloads = payload_manager.payloads[PayloadSource.CUSTOM.value]
    assert len(custom_payloads) > 0
    payload = custom_payloads[-1]
    assert payload.content == content
    assert payload.category == category
    assert payload.description == description

def test_get_payloads_by_source(payload_manager):
    """Test getting payloads filtered by source"""
    # Add test payloads
    payload_manager.add_custom_payload("test1", "category1")
    payload_manager.add_custom_payload("test2", "category2")
    
    payloads = payload_manager.get_payloads(source=PayloadSource.CUSTOM.value)
    assert len(payloads) > 0
    assert all(p.source == PayloadSource.CUSTOM.value for p in payloads)

def test_get_payloads_by_category(payload_manager):
    """Test getting payloads filtered by category"""
    category = "test_category"
    payload_manager.add_custom_payload("test1", category)
    payload_manager.add_custom_payload("test2", category)
    
    payloads = payload_manager.get_payloads(category=category)
    assert len(payloads) > 0
    assert all(p.category == category for p in payloads)

def test_search_payloads(payload_manager):
    """Test searching payloads"""
    payload_manager.add_custom_payload("admin' --", "auth_bypass")
    payload_manager.add_custom_payload("UNION SELECT", "union_based")
    
    results = payload_manager.search_payloads("UNION")
    assert len(results) > 0
    assert all("UNION" in p.content for p in results)

def test_get_available_sources(payload_manager):
    """Test getting available payload sources"""
    sources = payload_manager.get_available_sources()
    assert isinstance(sources, list)
    assert len(sources) > 0
    assert all(source in [s.value for s in PayloadSource] for source in sources)

def test_get_available_categories(payload_manager):
    """Test getting available payload categories"""
    categories = ["auth_bypass", "union_based", "blind"]
    for category in categories:
        payload_manager.add_custom_payload(f"test_{category}", category)
    
    available_categories = payload_manager.get_available_categories()
    assert isinstance(available_categories, list)
    assert len(available_categories) > 0
    assert all(category in available_categories for category in categories)

@pytest.mark.asyncio
async def test_deepseek_analysis(payload_manager):
    """Test Deepseek integration for payload analysis"""
    payload_content = "' UNION SELECT password FROM users--"
    
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json = Mock(
            return_value={
                "analysis": {
                    "type": "union_based",
                    "risk_level": "high",
                    "target_tables": ["users"],
                    "explanation": "This payload attempts to extract passwords"
                }
            }
        )
        
        result = await payload_manager.analyze_with_deepseek(
            payload_content,
            "sk-1bd5de3f31db429cb8cbe73875537c5c"
        )
        
        assert result is not None
        assert "analysis" in result
        assert "type" in result["analysis"]
        assert "risk_level" in result["analysis"]

    @pytest.mark.asyncio
    async def test_load_from_source_errors(payload_manager):
        """Test error handling in _load_from_source"""
        # Clear existing payloads
        payload_manager.payloads[PayloadSource.FUZZDB.value] = []

        # Mock aiohttp.ClientSession to control all requests
        async def mock_session_context():
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 404
            mock_response.text = AsyncMock(return_value="Not Found")
            mock_session.get.return_value.__aenter__.return_value = mock_response
            return mock_session

        with patch('aiohttp.ClientSession', side_effect=mock_session_context):
            await payload_manager._load_from_source(PayloadSource.FUZZDB)
            assert len(payload_manager.payloads[PayloadSource.FUZZDB.value]) == 0

        # Test network error
        async def mock_session_error():
            mock_session = AsyncMock()
            mock_session.get.side_effect = Exception("Network error")
            return mock_session

        with patch('aiohttp.ClientSession', side_effect=mock_session_error):
            await payload_manager._load_from_source(PayloadSource.FUZZDB)
            assert len(payload_manager.payloads[PayloadSource.FUZZDB.value]) == 0

        # Test invalid source configuration
        invalid_source = PayloadSource("invalid")
        await payload_manager._load_from_source(invalid_source)
        assert len(payload_manager.payloads[PayloadSource.FUZZDB.value]) == 0

    @pytest.mark.asyncio
    async def test_load_custom_payloads_errors(payload_manager, tmp_path):
        """Test error handling in _load_custom_payloads"""
        custom_path = os.path.join(tmp_path, "custom_payloads.json")
        
        # Save initial state
        initial_payloads = len(payload_manager.payloads[PayloadSource.CUSTOM.value])

        # Test invalid JSON
        with open(custom_path, 'w') as f:
            f.write("invalid json")
        
        with patch('os.path.dirname') as mock_dirname:
            mock_dirname.return_value = str(tmp_path)
            await payload_manager._load_custom_payloads()
            assert len(payload_manager.payloads[PayloadSource.CUSTOM.value]) == initial_payloads

        # Test empty file
        with open(custom_path, 'w') as f:
            f.write("")
        
        with patch('os.path.dirname') as mock_dirname:
            mock_dirname.return_value = str(tmp_path)
            await payload_manager._load_custom_payloads()
            assert len(payload_manager.payloads[PayloadSource.CUSTOM.value]) == initial_payloads

        # Test missing required fields
        with open(custom_path, 'w') as f:
            json.dump([{"invalid": "data"}], f)
        
        with patch('os.path.dirname') as mock_dirname:
            mock_dirname.return_value = str(tmp_path)
            await payload_manager._load_custom_payloads()
            assert len(payload_manager.payloads[PayloadSource.CUSTOM.value]) == initial_payloads

        # Test invalid data type
        with open(custom_path, 'w') as f:
            json.dump({"not": "a list"}, f)
        
        with patch('os.path.dirname') as mock_dirname:
            mock_dirname.return_value = str(tmp_path)
            await payload_manager._load_custom_payloads()
            assert len(payload_manager.payloads[PayloadSource.CUSTOM.value]) == initial_payloads

def test_error_handling(payload_manager):
    """Test error handling in payload operations"""
    # Test invalid source
    with pytest.raises(ValueError, match="Invalid source"):
        payload_manager.get_payloads(source="invalid_source")
    
    # Test invalid payload content
    with pytest.raises(ValueError, match="Content must be a non-empty string"):
        payload_manager.add_custom_payload(None)
    
    # Test empty string payload
    with pytest.raises(ValueError, match="Content must be a non-empty string"):
        payload_manager.add_custom_payload("")
    
    # Test file operation errors
    with patch('builtins.open', side_effect=IOError("Test IO error")):
        with pytest.raises(IOError, match="Test IO error"):
            payload_manager._save_custom_payloads()

def test_search_payloads_edge_cases(payload_manager):
    """Test edge cases in search_payloads"""
    # Test empty query
    results = payload_manager.search_payloads("")
    assert len(results) == 0

    # Test no matches
    payload_manager.add_custom_payload("test payload", "test")
    results = payload_manager.search_payloads("nonexistent")
    assert len(results) == 0

    # Test case insensitivity
    payload_manager.add_custom_payload("UPPER CASE", "test")
    results = payload_manager.search_payloads("upper")
    assert len(results) == 1
    results = payload_manager.search_payloads("UPPER")
    assert len(results) == 1

def test_custom_payloads_persistence(payload_manager, tmp_path):
    """Test saving and loading custom payloads"""
    # Add test payloads
    payload_manager.add_custom_payload("test1", "category1")
    payload_manager.add_custom_payload("test2", "category2")
    
    # Save payloads
    custom_path = os.path.join(tmp_path, "custom_payloads.json")
    with patch('os.path.dirname') as mock_dirname:
        mock_dirname.return_value = str(tmp_path)
        payload_manager._save_custom_payloads()
    
    # Verify file exists and content is correct
    assert os.path.exists(custom_path)
    with open(custom_path, 'r') as f:
        saved_data = json.load(f)
        assert len(saved_data) == 2
        assert all(isinstance(item, dict) for item in saved_data)
