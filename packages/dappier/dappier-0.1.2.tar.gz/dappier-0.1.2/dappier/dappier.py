import os
from typing import Optional
from dappier.types import AIModelResponse, AIModelRequest, REAL_TIME_AI_MODEL, POLYGON_STOCK_MARKET_AI_MODEL
from dappier.api.ai_models import AIModels


class Dappier:
    def __init__(self, api_key: Optional[str] = None) -> None:
        # First check if the api_key is provided directly
        if api_key is None:
            # If not, try to get it from the environment variable
            api_key = os.getenv("DAPPIER_API_KEY")

            # If the api_key is still None, prompt the user or raise an error
            if api_key is None:
                raise ValueError("API key must be provided either as an argument or through the environment variable DAPPIER_API_KEY.")

        self.api_key = api_key
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
          }

    def real_time_search_api(self, query: str) -> AIModelResponse:
        ai_models = AIModels(ai_model_id=REAL_TIME_AI_MODEL, headers=self._headers)
        request = AIModelRequest(query=query)
        return ai_models.search_ai_models(request=request)
    
    def polygon_stock_market_search_api(self, query):
        ai_models = AIModels(ai_model_id=POLYGON_STOCK_MARKET_AI_MODEL, headers=self._headers)
        request = AIModelRequest(query=query)
        return ai_models.search_ai_models(request=request)
        

    def __repr__(self) -> str:
        return f"Dappier(api_key={self.api_key[:4]}...)"  # Mask part of the key for privacy
