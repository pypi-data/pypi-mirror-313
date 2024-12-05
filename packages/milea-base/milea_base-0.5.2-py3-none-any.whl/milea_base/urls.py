from django.urls import path
from django.urls import include

app_name = "milea_base"

urlpatterns = [
    path("notify/", include("milea_notify.urls")),
]
