import requests
from .exceptions import APIError

BASE_URL = "https://v1.fastpix.io"

def make_request(method, endpoint, headers=None, data=None, params=None):
    """
    Generic request method to handle different HTTP methods.
    
    Args:
        method (str): HTTP method (GET, POST, PATCH, DELETE, etc.)
        endpoint (str): API endpoint
        headers (dict, optional): Request headers
        data (dict, optional): Request payload
        params (dict, optional): Query parameters
    
    Returns:
        dict: JSON response from the API
    
    Raises:
        APIError: For API-related errors
    """
    url = f"{BASE_URL}{endpoint}"
    headers = headers or {}

    try:
        # Dispatch to appropriate request method
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Check response status
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise APIError(f"Error: {response.status_code} - {response.text}")
    
    except requests.RequestException as e:
        raise APIError(f"Request failed: {str(e)}")
        