import requests
from typing import Dict, Optional, Union
from tabulate import tabulate
import json

# Base URLs for the API
BASE_URL = "https://api.opmentis.xyz/api/v1"
FOODBOT_URL = "https://labfoodbot.opmentis.xyz/api/v1"




def get_headers(token: str) -> Dict[str, str]:
    """
    Generate headers for authenticated requests.
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def send_request(method: str, url: str, **kwargs) -> Optional[Union[Dict, str]]:
    """
    Send an HTTP request and handle common errors.
    Args:
        method (str): HTTP method (e.g., GET, POST).
        url (str): The API endpoint URL.
        kwargs: Additional arguments for the request (e.g., headers, json).
    Returns:
        Optional[Union[Dict, str]]: Parsed response or None on failure.
    """
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed. Error: {e.response.status_code if e.response else 'Unknown Error'}")
        return None


def get_active_lab() -> Optional[Dict]:
    """
    Fetch the active lab details from the central API endpoint.
    """
    endpoint = f"{BASE_URL}/labs/labs/active"
    return send_request("GET", endpoint)

def authenticate(wallet_address: str) -> Optional[str]:
    """
    Authenticate a user based on their wallet address.
    Returns an authentication token if successful.
    """
    endpoint = f"{BASE_URL}/authenticate"
    params = {"wallet_address": wallet_address}
    response = send_request("POST", endpoint, params=params)
    return response.get("access_token") if response else None

def register_user(wallet_address: str, labid: str, role_type: str) -> Dict[str, Union[str, Dict]]:
    """
    Register a user as a miner or validator and add a stake for them.
    """
    # Authenticate the user
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication failed. Could not obtain access token."}

    # Prepare headers with the token
    headers = get_headers(token)

    # Define endpoints for registration and adding stake
    register_endpoint = f"{BASE_URL}/labs/labs/{labid}/{role_type}/register"
    add_stake_endpoint = f"{BASE_URL}/stakes/add"

    # Prepare payload for adding stake
    add_stake_payload = {
        "labid": labid,
        "minerstake": 0 if role_type == "miner" else 0,
        "validatorstake": 20 if role_type == "validator" else 0
    }

    # Add stake
    stake_response = send_request("POST", add_stake_endpoint, json=add_stake_payload, headers=headers)
    if not stake_response:
        return {"error": f"Failed to add stake for {role_type}."}

    # Prepare payload for registration
    register_payload = {"wallet_address": wallet_address}
    registration_response = send_request("POST", register_endpoint, json=register_payload, headers=headers)
    if not registration_response:
        return {"error": f"Failed to register as {role_type}."}

    # Parse the registration response body
    try:
        response_body = registration_response["message"]["body"]
        parsed_body = json.loads(response_body)  # Convert the JSON string to a dictionary

        # Extract the status and message to return a user-friendly message
        if parsed_body.get("status") == "success":
            return {
                "status": "success",
                "message": parsed_body.get("message"),
            }
        else:
            return {
                "status": "failure",
                "message": parsed_body.get("message", "Unknown error occurred."),
            }
    except (KeyError, json.JSONDecodeError) as e:
        return {
            "error": "Failed to parse registration response.",
            "details": str(e)
        }

def fetch_user_data(endpoint: str, wallet_address: str) -> Union[Dict, str]:
    """
    Fetch user data or points from a specified endpoint.
    """
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication required to fetch user data."}

    headers = get_headers(token)
    payload = {"wallet_address": wallet_address}
    response = send_request("POST", endpoint, json=payload, headers=headers)
    return response if response else {"error": "Failed to fetch user data."}


def render_table(wallet_address: str, data: Union[Dict, str]) -> str:
    """
    Render user data as a formatted table.
    Args:
        wallet_address (str): The wallet address of the user.
        data (Union[Dict, str]): The user data to be formatted.
    Returns:
        str: A formatted table as a string or raw string data if already formatted.
    """
    if isinstance(data, dict):
        # Convert dictionary data into a table format
        table_data = [[key, value] for key, value in data.items()]
        return tabulate(table_data, headers=[wallet_address, "Value"], tablefmt="grid")
    elif isinstance(data, str):
        # If the data is already a string (e.g., raw table), return it as is
        return data
    return "Invalid data format. Unable to render table."


def userdata(labid: str, wallet_address: str) -> Union[str, Dict]:
    """
    Fetch user data and return it as a formatted table or raw string.
    Args:
        labid (str): The lab ID to validate registration.
        wallet_address (str): The wallet address of the user.
    Returns:
        Union[str, Dict]: A formatted table as a string or an error message.
    """
    # Validate user registration and requirements
    validation_error = validate_user_registration(labid, wallet_address)
    if validation_error:
        return validation_error

    endpoint = f"{FOODBOT_URL}/user_data/table"
    payload = {"wallet_address": wallet_address}
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to fetch user data."

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()

        user_table = response.json().get("user_table", "")
        return render_table(wallet_address, user_table)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch user data. Error: {e}")
        return "Failed to fetch user data."



def userpoint(labid: str, wallet_address: str) -> str:
    """
    Fetch user points from the API and return as a formatted table.
    Args:
        labid (str): The lab ID to validate registration.
        wallet_address (str): The user's wallet address.
    Returns:
        str: Formatted table or error message.
    """
    # Validate user registration and requirements
    validation_error = validate_user_registration(labid, wallet_address)
    if validation_error:
        return validation_error

    endpoint = f"{BASE_URL}/labs/get-user-point"
    payload = {"labid": labid, "wallet_address": wallet_address}
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to fetch user points."

    headers = get_headers(token)
    response = send_request("POST", endpoint, json=payload, headers=headers)
    if response:
        user_table = response.get("user_data", {})
        return render_table(wallet_address, user_table)
    return "Failed to fetch user points."



def endchat() -> Union[str, Dict]:
    """
    End the chat session and trigger evaluation.
    """
    endpoint = f"{FOODBOT_URL}/end_chat"
    response = send_request("POST", endpoint)
    return response.get("message", "Chat ended and evaluation triggered.") if response else {"error": "Failed to end chat."}


def validate_user_registration(labid: str, wallet_address: str) -> Optional[str]:
    """
    Validate if a user is registered and meets the requirements for the specified lab.
    Args:
        labid (str): The lab ID to query.
        wallet_address (str): The wallet address of the user.
    Returns:
        Optional[str]: An error message if validation fails, otherwise None.
    """
    user_status = check_user_status(labid, wallet_address)

    # Check if user_status is an error message (string)
    if isinstance(user_status, str):
        return "Failed to fetch user status. Please ensure you are authenticated and registered."

    # If user_status contains an error key, return the error message
    if "error" in user_status:
        return user_status["error"]

    # Check if the user meets the miner or validator requirements
    if not user_status.get("meets_miner_requirements", False) and not user_status.get("meets_validator_requirements", False):
        return "You do not meet the requirements to access this lab. Please ensure you are registered and meet the minimum stake or balance requirements."

    return None  # Validation passed



def check_user_status(labid: str, wallet_address: str) -> Union[Dict, str]:
    """
    Check the user's stake status for a specific lab.
    Args:
        labid (str): The lab ID to query.
        wallet_address (str): The wallet address of the user.
    Returns:
        dict: Response from the API with user stake status.
    """
    # Authenticate the user to obtain a token
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication failed. Could not obtain access token."}

    # Construct the endpoint URL
    endpoint = f"{BASE_URL}/labs/labs/{labid}/wallets/{wallet_address}/status"
    
    # Set headers for the GET request
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    # Make the GET request to fetch the user status
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        user_status = response.json()
        return user_status
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to fetch user status."}
