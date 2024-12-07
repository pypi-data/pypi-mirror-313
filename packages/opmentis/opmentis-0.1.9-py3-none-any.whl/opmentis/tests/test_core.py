import pytest
import requests_mock
from opmentis import get_active_lab, authenticate, register_user, userdata, endchat

# Base URL for the API
BASE_URL = "https://api.opmentis.xyz/api/v1"



def test_get_active_lab():
    """Test fetching active lab details."""
    endpoint = f"{BASE_URL}/labs/labs/active"
    expected_response = {"lab_id": "active_lab_123", "requirements": {"stake": 20}}

    with requests_mock.Mocker() as m:
        m.get(endpoint, json=expected_response, status_code=200)
        response = get_active_lab()

        # Assertions
        assert response == expected_response, f"Expected {expected_response}, but got {response}"
        assert m.called, "The GET request was not called"

def test_authenticate():
    """Test user authentication."""
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/authenticate"
    expected_token = "mocked_token"

    with requests_mock.Mocker() as m:
        m.post(endpoint + f"?wallet_address={wallet_address}", json={"access_token": expected_token}, status_code=200)
        response = authenticate(wallet_address)
        
        assert response == expected_token, f"Expected token was '{expected_token}', but got '{response}'"

def test_register_user():
    """Test registering a user as a miner or validator and adding a stake."""
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    labid = "2631c92b-a020-4892-8dbc-059b5b36ed7e"
    role_type = "miner"
    
    authenticate_endpoint = f"{BASE_URL}/authenticate"
    register_endpoint = f"{BASE_URL}/labs/labs/{labid}/{role_type}/register"
    add_stake_endpoint = f"{BASE_URL}/stakes/add"
    
    expected_auth_token = "mocked_token"
    expected_registration_response = {"status": "success", "role_type": role_type, "wallet_address": wallet_address}
    expected_stake_response = {"status": "success", "message": "Stake added successfully."}
    
    with requests_mock.Mocker() as m:
        m.post(f"{authenticate_endpoint}?wallet_address={wallet_address}", json={"access_token": expected_auth_token}, status_code=200)
        m.post(register_endpoint, json=expected_registration_response, status_code=200)
        m.post(add_stake_endpoint, json=expected_stake_response, status_code=200)
        
        response = register_user(wallet_address, labid, role_type)
        
        assert m.call_count == 3, "Expected three API calls"
        expected_registration_payload = {
            "labid": labid,
            "minerstake": 20 if role_type == "miner" else 0,
            "validatorstake": 0
        }
        assert m.request_history[1].json() == expected_registration_payload, "The registration payload is incorrect"



def test_authenticate_failure():
    """Test failed authentication due to unregistered wallet address."""
    unregistered_wallet_address = "0xUnregisteredWallet"
    endpoint = f"{BASE_URL}/authenticate"
    expected_response = {"error": "Authentication failed. User not registered"}

    with requests_mock.Mocker() as m:
        m.post(endpoint, json=expected_response, status_code=404)
        response = authenticate(unregistered_wallet_address)
        
        assert response is None, "Expected None when authentication fails"

def test_userdata_success():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/user_data/table"
    expected_response = "Mocked table data"

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"user_table": expected_response}, status_code=200)
        response = userdata(wallet_address)
        
        # Assert response
        assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"
        
        # Assert last request payload
        assert m.last_request.json() == {"wallet_address": wallet_address}

def test_userdata_failure():
    wallet_address = "0x42C584058fA2a01622D09827EF688dD33d9643Dc"
    endpoint = f"{BASE_URL}/user_data/table"
    expected_response = {"error": "Failed to fetch user data."}  # Updated to match the actual response

    # Setup mock
    with requests_mock.Mocker() as m:
        m.post(endpoint, json={"error": "Failed to fetch user data."}, status_code=500)
        
        # Call the function and capture the response
        response = userdata(wallet_address)
        
        # Assert the response matches the expected response
        assert response == expected_response, f"Expected '{expected_response}', but got '{response}'"
        
        # Assert the payload sent in the last request
        assert m.last_request.json() == {"wallet_address": wallet_address}, "The payload is incorrect"

