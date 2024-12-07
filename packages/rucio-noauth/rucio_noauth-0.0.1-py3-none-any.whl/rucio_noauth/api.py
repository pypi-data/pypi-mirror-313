import json
import os

import requests

BASE_URL = os.getenv("RUCIO_NOAUTH_URL", "http://localhost:8012")  

def rucio_list_dids(scope: str, filters: list[dict[str, any]], did_type: str = 'collection', long: bool = True):
    """Call the `/list-dids` endpoint."""
    # Define query parameters
    params = {
        "scope": scope,
        "did_type": did_type,
        "long": str(long).lower(),  # Convert to lowercase for boolean query params
    }
    try:
        # Send the POST request with the filters as JSON body
        response = requests.post(
            f"{BASE_URL}/list-dids", 
            params=params, 
            json=filters  # Filters are passed as JSON in the request body
        )
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                try:
                    # Decode the line from bytes to string and parse JSON
                    did = json.loads(line.decode('utf-8'))
                    yield did
                except json.JSONDecodeError as e:
                    # Handle JSON parsing errors
                    yield {"error": f"JSON decode error: {str(e)}", "raw_line": line.decode('utf-8')}
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        yield {"error": f"Request failed: {str(e)}"}

def rucio_list_content(scope: str, name: str):
    """Call the `/list-dids` endpoint."""
    params = {
        "scope": scope,
        "name": name,
    }
    try:
        response = requests.get(f"{BASE_URL}/list-content", params=params)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                try:
                    # Decode the line from bytes to string and parse JSON
                    content = json.loads(line.decode('utf-8'))
                    yield content
                except json.JSONDecodeError as e:
                    # Handle JSON parsing errors
                    yield {"error": f"JSON decode error: {str(e)}", "raw_line": line.decode('utf-8')}
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        yield {"error": f"Request failed: {str(e)}"}

def rucio_list_file_replicas(
    dids: list[dict[str, str]],
    schemes: str = None,
    rse_expression: str = None,
    metalink: bool = False,
    all_states: bool = False,
    no_resolve_archives: bool = True,
    domain: str = None,
    sort: str =  None,
):
    """Call the `/list-file-replicas` endpoint."""
    # Prepare the parameters for the query
    params = {
        "schemes": schemes,
        "rse_expression": rse_expression,
        "metalink": metalink,
        "all_states": all_states,
        "no_resolve_archives": no_resolve_archives,
        "domain": domain,
        "sort": sort,
    }
    
    # Prepare the request body
    body = dids
    # Define the headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        # Send the POST request with JSON body and query params
        response = requests.post(f"{BASE_URL}/list-file-replicas", json=body, params=params, headers=headers)
        for line in response.iter_lines():
            if line:
                try:
                    # Decode the line from bytes to string and parse JSON
                    replicas = json.loads(line.decode('utf-8'))
                    yield replicas
                except json.JSONDecodeError as e:
                    # Handle JSON parsing errors
                    yield {"error": f"JSON decode error: {str(e)}", "raw_line": line.decode('utf-8')}
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        yield {"error": f"Request failed: {str(e)}"}


