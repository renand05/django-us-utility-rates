from django.contrib import admin
from django.urls import path
from utilities import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.WebsiteDemoView.as_view(template_name="website_demo.html")),
]
