import pytest
import requests
from django.contrib.auth.models import User

# giving pytest access to database.
pytestmark = pytest.mark.django_db


class TestRegistrationApp:
    def test_access(self):
        registration_url = 'http://127.0.0.1:8000/registration/'
        response = requests.get(registration_url)
        assert response.status_code == 200
