from django.urls import path
from . import views

urlpatterns = [
    path("", views.PingApi.as_view()),
]