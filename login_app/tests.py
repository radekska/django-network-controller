import pytest
from django.contrib.auth.models import User

# giving pytest access to database.
pytestmark = pytest.mark.django_db


class TestUsers:
    def test_super_user(self):
        super_user = User.objects.get(username='admin')
        assert super_user.is_superuser
