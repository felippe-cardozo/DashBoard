# arn:aws:s3:::dashboardforvoxus
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Task, Document

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


class TestViews(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.user = User(username='user')
        self.user.set_password('password')
        self.user.save()
        Client.login(username=self.user.username, password='password')
        self.task = Task.objects.last()

    def test_get_update_view(self):
        update_url = '/update' + str(self.task.pk)
        c = Client()
        res = c.get(update_url)
        self.assertEqual(res.status_code, 200)

    def test_get_detail_view(self):
        detail_url = '/task'



class TestTasks(TestCase):
    fixtures = ['fixtures.json']

    def test_generate_list_of_documents(self):
        task = Task.objects.last()
        listed_documents = task.list_documents()
        self.assertEqual(task.document_set.count(), len(listed_documents))
