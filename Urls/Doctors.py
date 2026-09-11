from django.urls import path
from Views.DoctorView import DoctorListCreateView, DoctorDetailView


urlpatterns = [
    path("", DoctorListCreateView.as_view()),
    path("<int:pk>/", DoctorDetailView.as_view()),
]