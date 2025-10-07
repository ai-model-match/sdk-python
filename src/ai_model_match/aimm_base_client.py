import requests
from typing import Optional

class AIMMBaseClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }

    def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()