from django.urls import path
from postcodes.views import address_check_api

app_name = "postcodes"

urlpatterns = [
    path("api/", address_check_api, name="api"),
]