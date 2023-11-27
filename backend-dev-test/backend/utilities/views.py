from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from pydantic import BaseModel, Field
from typing import Optional
from utilities.services import UtilityRatesServiceBase, UtilityRatesService


OPENEI_UTILITY_RATES_ORDERBY_PARAM = 'startdate'
OPENEI_FULL_DETAIL_PARAM = 'full'
OPENEI_LIMIT_PARAM = 1

class WebsiteDemoUserInput(BaseModel):
    user_address: Optional[str]
    user_consumption: Optional[str]
    user_percentage_scale: Optional[str]

class OpenEiParams(BaseModel):
    detail: str = Field(default=OPENEI_FULL_DETAIL_PARAM)
    address: str
    limit: str = Field(default=OPENEI_LIMIT_PARAM)
    format: str = 'json'
    approved: bool = 'true'
    is_default: bool = 'true'
    orderby: str = Field(default=OPENEI_UTILITY_RATES_ORDERBY_PARAM)
    direction: str = 'desc'

class WebsiteDemoView(TemplateView):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'website_demo.html', {
            'new_user_address': 'user address',
            'new_user_consumption': 'user consumption',
            'new_user_percentage_scale': 'user percentage scale',
        })

    def post(self, request: HttpRequest, service: UtilityRatesServiceBase = UtilityRatesService()) -> HttpResponse:
        user_input = WebsiteDemoUserInput.model_validate(request.POST.dict())
        openei_params = OpenEiParams(address=user_input.user_address)
        service.user_params = openei_params.model_dump()
        user_results = service.get_openei_results()
        print('>>>>>>>>>>>>>> user results', user_results)
        return render(request, 'website_demo.html', {
            'new_user_address': user_input.user_address,
            'new_user_consumption': user_input.user_consumption,
            'new_user_percentage_scale': user_input.user_percentage_scale,
        })
