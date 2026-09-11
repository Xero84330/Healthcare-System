from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from Apps.Patient.models import Patient

User = get_user_model()

class PatientOwnershipTests(APITestCase):

    def setUp(self):
        self.alice = User.objects.create_user(email="alice@example.com", name="Alice", password="pass12345")
        self.eve = User.objects.create_user(email="eve@example.com", name="Eve", password="pass12345")
        self.patient = Patient.objects.create(name="Alice's Patient", created_by=self.alice)

    def test_owner_can_see_their_patient(self):
        self.client.force_authenticate(user=self.alice)
        res = self.client.get(f"/api/patients/{self.patient.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_other_user_gets_404_not_someone_elses_patient(self):
        self.client.force_authenticate(user=self.eve)
        res = self.client.get(f"/api/patients/{self.patient.id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_is_rejected(self):
        res = self.client.get("/api/patients/")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
