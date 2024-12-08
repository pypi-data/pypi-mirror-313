import requests
import json
from dappier.types import (
  BASE_URL,
  AIModelRequest,
  AIModelResponse
)

class AIModels:
  def __init__(self, headers: dict[str, str]) -> None:
    self._baseUrl = f"{BASE_URL}/app/aimodel"
    self.headers = headers

  def search_ai_models(self, ai_model_id: str, request: AIModelRequest) -> AIModelResponse:
        # Convert the request object to a dictionary directly
        request_data = {"query": request.query}
        
        # Send the POST request
        response = requests.post(
            f"{self._baseUrl}/{ai_model_id}",
            headers=self.headers,
            data=json.dumps(request_data)  # Directly serialize the request data
        )
        
        # Check the status code, raise an error if it's not 200
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        
        # If the request is successful, parse the response
        response_data = response.json()
        return AIModelResponse(message=response_data.get("message"))
