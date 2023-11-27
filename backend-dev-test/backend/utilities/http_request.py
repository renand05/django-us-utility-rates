from abc import ABC, abstractmethod
import requests
import json

from typing import Dict
from typing_extensions import Self

from utilities.tests.mocks.openei_utility_rates_response_mock import OPENEI_RESPONSE_MOCK

class HttpRequestBuilderBase(ABC):
    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self.params = {}

    @abstractmethod
    def add_param(self) -> Dict:
        pass

    @abstractmethod
    def execute(self, key, value) -> json:
        pass

class HttpRequestBuilder(HttpRequestBuilderBase):
    def add_param(self, key, value) -> Self:
        self.params[key] = value

        return self

    def execute(self) -> json:
        response = requests.get(self.base_url, params=self.params)

        return response.json()

class FakeHttpRequestBuilder(HttpRequestBuilderBase):
    def add_param(self, key, value):
        self.params[key] = value

        return self

    def execute(self) -> json:
        fake_response = OPENEI_RESPONSE_MOCK

        return fake_response
