import pytest
import requests
import unittest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager



# giving pytest access to database.
pytestmark = pytest.mark.django_db


class TestRegistrationView(TestCase):
    def test_get_request(self):
        url = reverse('registration')
        response = self.client.get(url)

        assert response.status_code == 200


class TestRegistrationSignUp(unittest.TestCase):
    def test_post_request(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        self.driver.get("http://localhost:8000/registration/")
        self.driver.find_element_by_id('username').send_keys("test_username")
        self.driver.find_element_by_id('password1').send_keys("Test_password123")
        self.driver.find_element_by_id('password2').send_keys("Test_password123")

        self.driver.find_element_by_id('submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

        created_user = User.objects.get(username='test_username')
        self.assertEqual(created_user.username, 'test_username')
        self.assertEqual(isinstance(created_user.password, str), True)


