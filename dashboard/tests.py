# arn:aws:s3:::dashboardforvoxus
from django.test import TestCase, Client
from django.contrib.auth.models import User
import mock
from .models import Task


def mocked_remove_from_s3(*args):
    return


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
        self.assertContains(res, 'DashBoard', status_code=200)


class TestViews(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.user = User(username='user')
        self.user.set_password('password')
        self.user.save()
        self.task = Task.objects.last()
        self.c = Client()
        self.c.login(username='user', password='password')

    def test_get_update_view(self):
        update_url = '/update/' + str(self.task.pk) + '/'
        res = self.c.get(update_url)
        self.assertContains(res, self.task.name, status_code=200)

    def test_get_detail_view(self):
        detail_url = '/task/' + str(self.task.pk) + '/'
        res = self.c.get(detail_url)
        self.assertContains(res, self.task.description, status_code=200)

    def test_post_new_task(self):
        new_url = '/new/'
        count = Task.objects.all().count()
        self.c.post(new_url, {'name': 'TestTask',
                              'description': 'TestDescription',
                              'priority': 3})
        self.assertEqual(Task.objects.last().name, 'TestTask')
        self.assertEqual(Task.objects.last().description, 'TestDescription')
        self.assertEqual(Task.objects.last().priority, 3)
        self.assertEqual(Task.objects.all().count(), count + 1)

    def test_update_task(self):
        update_url = '/update/' + str(self.task.pk) + '/'
        self.c.post(update_url, {'name': 'newname',
                                 'description': 'newdescription',
                                 'priority': 1})
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(task.name, 'newname')
        self.assertEqual(task.description, 'newdescription')

    @mock.patch('dashboard.models.Task.remove_from_s3',
                new=mocked_remove_from_s3)
    def test_destroy_task(self):
        count = Task.objects.all().count()
        destroy_url = '/destroy/' + str(self.task.id) + '/'
        self.c.post(destroy_url)
        self.assertEqual(Task.objects.all().count(), count - 1)


class TestTasks(TestCase):
    fixtures = ['fixtures.json']

    def test_generate_list_of_documents(self):
        task = Task.objects.last()
        listed_documents = task.list_documents()
        self.assertEqual(task.document_set.count(), len(listed_documents))
