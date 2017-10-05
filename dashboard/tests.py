# arn:aws:s3:::dashboardforvoxus
from django.test import TestCase, Client
from django.contrib.auth.models import User

class TestGoogleLogin(TestCase):
    def setUp(self):
        self.user = User(username='user')
        self.user.set_password('password')
        self.user.save()

    # assert that if user is not logged in it gets redirected
    def test_login_required(self):
        c = Client()
        res = c.get('/')
        self.assertEqual(res.status_code, 302)

    def test_logged_user_gets_dashboard(self):
        c = Client()
        c.login(username=self.user.username, password='password')
        res = c.get('/')
        self.assertEqual(res.status_code, 200)
