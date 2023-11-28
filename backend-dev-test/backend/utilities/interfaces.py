from pydantic import BaseModel, Field
from typing import List

class UserInput(BaseModel):
    address: str
    consumption: int = Field(ge=10, le=1000)
    percentage_scale: int


class MostLikelyUtility(BaseModel):
    label: str
    name: str
    price: float
    utility: str
    eiaid: int


class OpenEiProcessorResponse(BaseModel):
    average_rate: float
    most_likely_utility: MostLikelyUtility
    utilities: List
