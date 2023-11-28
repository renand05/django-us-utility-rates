import json
import numpy as np

from pydantic import BaseModel
from typing import List, Optional

from utilities.interfaces import UserInput, OpenEiProcessorResponse, MostLikelyUtility

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
    energyweekdayschedule: Optional[List[List[int]]]
    fixedmonthlycharge: float

    class Config:
        ignore = True


class ProcessorResponse:
    def process_response(self, openei_response: json, user_input: UserInput):
        raise NotImplementedError("Subclasses must implement process_response")


class OpenEiProcessor(ProcessorResponse):
    hourly_load_charge_consumption_percentage = np.array([0.3, 0.28, 0.25, 0.23, 0.2, 0.2, 0.22, 0.3, 0.4, 0.42, 0.45, 0.5, 0.5, 0.55, 0.6, 0.6, 0.55, 0.5, 0.6, 0.85, 1, 0.9, 0.75, 0.53])

    def parse_openei_response(self, openei_response: json) -> List[UtilityItem]:
        items_list = openei_response.get('items', [])

        return [UtilityItem.model_validate(item) for item in items_list]

    """average rate 
        mode 1: average based on rates structure period rates
    """
    def compute_average_rate_mode_1(self, energy_rates_structure: List[List[UtilityPeriodRate]]) -> float:
        rate_sum = 0
        for item in energy_rates_structure:
            for rate in item:
                rate_sum += rate.rate
        avg_rate = rate_sum/len(energy_rates_structure)
        return avg_rate

    """average rate
        mode 2: average based on weekdays schedule distributions
            average taking into account the weekdays schedule weights
            and period rates 
    """
    def get_average_rate_mode_2(self, energy_rates_structure: List[List[UtilityPeriodRate]], energy_weekdayschedule: List[List[int]]) -> float:
        pass 

    def process_response(self, openei_response: json, user_input: UserInput) -> OpenEiProcessorResponse:
        utility_rates = self.parse_openei_response(openei_response=openei_response)
        hourly_average_rates_cost = []
        user_rates_cost = []

        for rate in utility_rates:
            hourly_average_rates_cost.append(self.compute_average_rate_mode_1(energy_rates_structure=rate.energyratestructure))
        average_rates_cost = np.array(hourly_average_rates_cost)

        for average_rate in average_rates_cost:
            user_rates_cost.append(average_rate*user_input.consumption*self.hourly_load_charge_consumption_percentage)
        user_costs = np.array(user_rates_cost)

        average_user_rate = np.mean(user_costs, axis=1)
        minimum_rate_utility_tariff = utility_rates[np.argmin(average_user_rate)]
        most_likely_utility = MostLikelyUtility(
            label=minimum_rate_utility_tariff.label,
            name=minimum_rate_utility_tariff.name,
            price=minimum_rate_utility_tariff.fixedmonthlycharge,
            utility=minimum_rate_utility_tariff.utility,
            eiaid=minimum_rate_utility_tariff.eiaid
        )
        return OpenEiProcessorResponse(
            average_rate=round(most_likely_utility.price, 2),
            most_likely_utility=most_likely_utility,
            utilities=utility_rates
        )
