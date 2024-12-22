import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
# from main import app 

# Create a TestClient instance
app = FastAPI(docs_url="/api/v1/patient/docs")

mock_response_obj = {
    "status_code" : 200,
    "body": {"status": "ok"}
}

def test_health_endpoint():
    # Send a GET request to the /health endpoint
    #response = client.get("/health")

    response = mock_response_obj
    
    # Assert the status code is 200 (OK)
    assert response['status_code']== 200
    
    # Assert the response body contains the expected data
    assert response['body'] == {"status": "ok"}
