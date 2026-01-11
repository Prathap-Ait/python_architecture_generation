# auth_utils.py
import json
import boto3
import jwt
from functools import lru_cache
from botocore.exceptions import ClientError


@lru_cache(maxsize=1)
def get_secret(secret_name: str) -> str:
    """
    Retrieve secret from AWS Secrets Manager with caching.
    Uses lru_cache to avoid repeated API calls within the same Lambda container.
    """
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response["SecretString"]
        # Handle JSON-formatted secrets
        
        try:
            secret_data = json.loads(secret_string)
            # If stored as {"JWT_SECRET": "actual_value"}
            return secret_data.get(secret_name, secret_string)
        except json.JSONDecodeError:
            # Plain string secret
            return secret_string
            
    except ClientError as e:
        raise Exception(f"Failed to retrieve secret: {e}")


def verify_jwt(event: dict) -> dict:
    """
    Verify JWT token from Lambda event headers.
    
    Args:
        event: Lambda event object with headers
        
    Returns:
        dict: {
            "success": True, "accountId": str, "cloudId": str
        } on success, or
        {
            "success": False, "error": str
        } on failure
    """
    # Extract token from headers (handle case-insensitive headers)
    headers = event.get("headers") or {}
    token = headers.get("token") or headers.get("Token")
    
    if not token:
        return {"success": False, "error": "Unauthorized"}
    
    try:
        # Fetch secret key from Secrets Manager
        secret_key = get_secret("JWT_SECRET")
        
        # Decode and verify JWT
        decoded = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"]  # Specify allowed algorithms explicitly
        )
        
        return {
            "success": True,
            "accountId": decoded.get("accountId"),
            "cloudId": decoded.get("cloudId"),
        }
        
    except jwt.ExpiredSignatureError:
        return {"success": False, "error": "Token has expired"}
    except jwt.InvalidTokenError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    test_token = "eyJhbGciOiJIUiIsInR5cCI6IkpXVCJ9.eyJjbG91ZElkIjoiMWRjNTQ4ZTktOTQ4Yy00MTRhLWE4NWMtZjY5ZDQzNTY0NzdjIiwiYWNjb3VudElkIjoiNzEyMDIwOjY5MWZhMzNkLTljZjctNDA3ZC05MGYxLTRhYjRlNzJjNTUxMiIsInNpdGVVcmwiOiJwcmF0aGFwMDgwMy5hdGxhc3NpYW4ubmV0IiwiaWF0IjoxNzY0ODMwODU4LCJleHAiOjE3NjQ4MzQ0NTh9.OHX6FpryjWG6LztVd-EQFZ3DfAyTWFR0S8n_8vTRgtE"  # Replace with a valid JWT token
    event = {
        "headers": {
            "token": test_token
        }
    }
    result = verify_jwt(event)
    print(result)
