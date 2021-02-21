import pytest
from main_app import settings
from django.contrib.auth.models import User

# Telling pytest to use current database for tests.
# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': settings.BASE_DIR / 'db.sqlite3'
#     }


