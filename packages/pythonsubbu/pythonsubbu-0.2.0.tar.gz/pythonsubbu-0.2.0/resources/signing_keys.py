from .exceptions import APIError
from .api import make_request

class SigningKeysResource:
    def __init__(self, client):
        self.client = client
    
    def create(self):
        """Create a signing key."""
        try:
            return make_request(
                method="POST", 
                endpoint="/iam/signing-keys", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to create signing key: {str(e)}")

    def list(self):
        """Fetch a list of signing keys."""
        try:
            return make_request(
                method="GET", 
                endpoint="/iam/signing-keys", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to fetch signing keys: {str(e)}")

    def delete(self, signing_key_id):
        """Delete a specific signing key by its ID."""
        if not signing_key_id:
            raise ValueError("Signing key ID must be provided.")
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/iam/signing-keys/{signing_key_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to delete signing key: {str(e)}")

    def get(self, signing_key_id):
        """Fetch details of a specific signing key by its ID."""
        if not signing_key_id:
            raise ValueError("Signing key ID must be provided.")
        
        try:
            return make_request(
                method="GET", 
                endpoint=f"/iam/signing-keys/{signing_key_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to fetch signing key details: {str(e)}")
            