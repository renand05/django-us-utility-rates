from typing import List, Dict, Optional
from pydantic import BaseModel

class UtilityPeriodRate(BaseModel):
    rate: float

    class Config:
        ignore = True


class UtilityItem(BaseModel):
    label: str
    utility: str
    eiaid: int
    name: str
    startdate: int
    sector: str
    flatdemandunit: str
    energyratestructure: List[List[UtilityPeriodRate]]
    flatdemandmonths: Optional[List]
    energyweekdayschedule: Optional[List]
    energyweekendschedule: Optional[List]
    fixedmonthlycharge: float

    class Config:
        ignore = True


class ResponseProcessor:
    def process_response(self, response_data):
        raise NotImplementedError("Subclasses must implement process_response")


class OpenEiProcessor(ResponseProcessor):
    def parse_openei_response(self, openei_response) -> List[UtilityItem]:
        items_list = openei_response.get('items', [])

        return [UtilityItem.model_validate(item) for item in items_list]

    def process_response(self, openei_response: Dict) -> List[UtilityItem]:
        print('>>>>>>>>>>>>>>>>>> response', openei_response)
        utility_rates = self.parse_openei_response(openei_response=openei_response)
        # TODO compute avg cost
        # TODO get the most common utility tariff
        # TODO list of utility tariffs to be displayed
        # TODO projection of cost for the first year
        return utility_rates
