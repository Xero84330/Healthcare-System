from django.urls import path
from Views import HelloApi

urlpatterns = [
    path("hello/", HelloApi.as_view()),
]