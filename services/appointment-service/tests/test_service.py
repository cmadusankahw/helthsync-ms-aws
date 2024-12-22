import pytest
from fastapi.testclient import TestClient
from main import app 

mock_response_obj = {
    "status_code" : 200,
    "body": {"status": "ok"}
}

client = TestClient(app)

def test_health_endpoint():
    # Send a GET request to the /health endpoint
    response = client.get("/api/v1/appointment/health")

    # response = mock_response_obj
    
    # Assert the status code is 200 (OK)
    assert response.status_code== 200
    
    # Assert the response body contains the expected data
    assert response.json()['message'] == {"status": "ok"}
