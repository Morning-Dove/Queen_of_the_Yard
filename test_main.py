from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from starlette.testclient import TestClient
from main import app
import requests


client = TestClient(app)








############################
# *** SQUARE PAYMENTS ***
############################


# TEST for list_payments():

@patch('main.requests.get')
def test_list_payments(mock_get):
    mock_response = {
        'payments': [
            {'id': "N660Kal63Svrcev0BFhBDclL9lNZY", 'amount': 100},
            {'id': "TTNksUg2Y2xZiTI0UYJqBIrPFWNZY", 'amount': 200}
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    response = client.get("/payments")

    assert response.status_code == 200
    assert response.json() == mock_response['payments']

@patch('main.requests.get')
def test_list_payments_error(mock_get):

    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "Payment not found"

    response = client.get("/payments")

    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}


# TEST for GetPayment():
def test_get_payment():
    payment_id = "N660Kal63Svrcev0BFhBDclL9lNZY"
    
    with MagicMock() as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200  # Set the status code according to your test case
        mock_response.json.return_value = {"detail": "Payment found with payment_id example_payment_id"}
        mock_get.return_value = mock_response
        app.dependency_overrides[requests.get] = mock_get
        
        response = client.get(f"/payments/{payment_id}")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Payment not found with payment_id example_payment_id"}


