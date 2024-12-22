import pytest
from fastapi.testclient import TestClient
from ..main import app  # Import your FastAPI app from the service

# Create a TestClient instance
client = TestClient(app)

def test_health_endpoint():
    # Send a GET request to the /health endpoint
    response = client.get("/health")
    
    # Assert the status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert the response body contains the expected data
    assert response.json() == {"status": "ok"}
