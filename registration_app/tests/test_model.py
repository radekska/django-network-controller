import pytest
from django.contrib.auth.models import User

# giving pytest access to database.
pytestmark = pytest.mark.django_db


class TestUserModel:
    def create_user(self):
        return User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                        password='pytest_password')

    def test_user_creation(self):
        test_user = self.create_user()
        assert isinstance(test_user, User)
        assert test_user.username == 'pytest_user'
        assert test_user.email == 'pytest_user@gmail.com'
        assert isinstance(test_user.password, str)
