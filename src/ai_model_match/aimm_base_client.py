import requests
from typing import Optional
from ai_model_match.aimm_exceptions import AIMMHTTPException, AIMMHTTPGenericException

class AIMMBaseClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }

    def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            data = None
            try:
                # Try to parse error response as JSON
                data = response.json()
            except Exception as e:
                # Not a JSON response, raise generic error
                raise AIMMHTTPGenericException(
                    message="An error occurred",
                    err=str(e)
                )
            # If we have valid JSON data, raise specific error
            raise AIMMHTTPException(
                status_code=response.status_code,
                errors=data.get('errors', [])
            )
        # Catch any other exceptions and raise a generic error
        except Exception as e:
            raise AIMMHTTPGenericException(
                message="An error occurred",
                err=str(e)
            )
        