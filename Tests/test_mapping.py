from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from Apps.Doctors.models.Doctors import Doctor

from Apps.Patient.models import Patient

User = get_user_model()

class MappingTests(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user(email="alice@example.com", name="Alice", password="pass12345")
        self.patient = Patient.objects.create(name="Some Patient", created_by=self.alice)
        self.doctor = Doctor.objects.create(name="Dr House", created_by=self.alice)
        self.client.force_authenticate(user=self.alice)

    def test_create_mapping(self):
        res = self.client.post("/api/mappings/", {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_duplicate_mapping_is_rejected(self):
        self.client.post("/api/mappings/", {"patient": self.patient.id, "doctor": self.doctor.id})
        res = self.client.post("/api/mappings/", {"patient": self.patient.id, "doctor": self.doctor.id})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
