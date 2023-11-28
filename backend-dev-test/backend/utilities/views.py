from django.http import HttpRequest, HttpResponse
from pydantic import BaseModel, Field, ValidationError

from utilities.interfaces import UserInput
from utilities.services import UtilityRatesServiceBase, UtilityRatesService

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated


OPENEI_UTILITY_RATES_ORDERBY_PARAM = 'startdate'
OPENEI_FULL_DETAIL_PARAM = 'full'
OPENEI_LIMIT_PARAM = 5


class OpenEiParams(BaseModel):
    detail: str = Field(default=OPENEI_FULL_DETAIL_PARAM)
    address: str
    limit: int = Field(default=OPENEI_LIMIT_PARAM)
    format: str = 'json'
    approved: str = 'true'
    is_default: str = 'true'
    orderby: str = Field(default=OPENEI_UTILITY_RATES_ORDERBY_PARAM)
    direction: str = 'desc'


class RatesDemoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest) -> HttpResponse:
        return Response({
            'new_user_address': 'user address',
            'new_user_consumption': 'user consumption',
            'new_user_percentage_scale': 'user percentage scale',
        })

    def post(self, request: HttpRequest, service: UtilityRatesServiceBase = UtilityRatesService()) -> HttpResponse:
        try:
            user_input = UserInput.model_validate_json(request.body.decode())
            openei_params = OpenEiParams(address=user_input.address)
            service.user_params = openei_params.model_dump()
            user_results = service.get_openei_results(user_input=user_input)
            return Response(user_results.model_dump())
        except ValidationError as error:
            raise APIException(error)