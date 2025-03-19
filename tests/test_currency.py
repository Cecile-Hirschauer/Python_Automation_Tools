import pytest
import requests
from unittest.mock import patch
from ..currency import currency_convert, CURRENCIES

# Données de test
MOCK_SUCCESS_RESPONSE = {
    "data": {
        "USD": 1.0,
        "EUR": 0.85,
        "CAD": 1.25,
        "GBP": 0.73,
        "INR": 74.5
    }
}

@pytest.fixture
def mock_api_response():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = MOCK_SUCCESS_RESPONSE
        mock_get.return_value.raise_for_status.return_value = None
        yield mock_get

def test_currency_convert_success(mock_api_response):
    """Test la conversion de devise avec une réponse API réussie"""
    result = currency_convert("USD")
    assert result == MOCK_SUCCESS_RESPONSE["data"]
    mock_api_response.assert_called_once()

def test_currency_convert_request_error():
    """Test la gestion des erreurs de requête API"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException()
        result = currency_convert("USD")
        assert result is None

def test_currencies_list():
    """Test la validité de la liste des devises"""
    expected_currencies = ["USD", "EUR", "CAD", "GBP", "INR"]
    assert CURRENCIES == expected_currencies
    assert len(CURRENCIES) == 5

def test_currency_convert_invalid_response():
    """Test la gestion d'une réponse API invalide"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"error": "Invalid response"}
        mock_get.return_value.raise_for_status.return_value = None
        result = currency_convert("USD")
        assert result is None