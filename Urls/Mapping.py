from django.urls import path
from Views.MappingView import (
    MappingListCreateView,
    MappingPatientView,
)


urlpatterns = [
    path("", MappingListCreateView.as_view()),
    path("<int:id>/", MappingPatientView.as_view()),
]