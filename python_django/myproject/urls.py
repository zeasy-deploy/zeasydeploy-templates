from django.urls import path
from myapp.views import ping

urlpatterns = [
    path('ping', ping),
]
