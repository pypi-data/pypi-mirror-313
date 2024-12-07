from typing import Any
import requests
from .auth import LocalvoltsAuth

class MarketData:
    def __init__(self, json_data):
        self.data = json_data['objResult']

    def __getattr__(self, item: str) -> Any:
        """
        This method is called when an attribute lookup has not found the attribute in the usual places.
        It allows access to the dictionary keys as if they were attributes.
        """
        try:
            return self.data[item]
        except KeyError:
            raise AttributeError(f"'MarketData' missing '{item}'")

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"MarketData({self.data})"

class MarketAPI:
    BASE_URL = "https://api.localvolts.com/v1"

    def __init__(self, auth: LocalvoltsAuth):
        """
        Initialize the MarketAPI class with LocalvoltsAuth instance.

        :param auth: LocalvoltsAuth - An instance of the LocalvoltsAuth class for handling authentication.
        """
        self.auth = auth

    def get_market_stats(self) -> MarketData:
        """
        Retrieve market statistics.

        :return: dict - The response data from the Localvolts API.
        """
        url = f"{self.BASE_URL}/market/stats"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        return MarketData(response.json())
