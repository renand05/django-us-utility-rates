from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from pydantic import BaseModel
from typing import Optional


class WebsiteDemoUserInput(BaseModel):
    user_address: Optional[str]
    user_consumption: Optional[str]
    user_percentage_scale: Optional[str]

class WebsiteDemoView(TemplateView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'website_demo.html', {
            'new_user_address': request.POST.get('user_address', ''),
            'new_user_consumption': request.POST.get('user_consumption', ''),
            'new_user_percentage_scale': request.POST.get('user_percentage_scale', ''),
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        user_input = WebsiteDemoUserInput.model_validate(request.POST.dict())
        return render(request, 'website_demo.html', {
            'new_user_address': user_input.user_address,
            'new_user_consumption': user_input.user_consumption,
            'new_user_percentage_scale': user_input.user_percentage_scale,
        })
