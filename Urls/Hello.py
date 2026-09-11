from django.urls import path
from Services import HelloApi

urlpatterns = [
    path("hello/", HelloApi.as_view()),
]