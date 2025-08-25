import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()

TEST_PASSWORD = 'letmeinplease'


@pytest.mark.django_db
class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_registration(self):
        initial_users = User.objects.count()

        url = reverse('users:create')
        user_data = {
            'username': 'test_user',
            'password1': 'qwerty123!!!',
            'password2': 'qwerty123!!!',
            'first_name': 'first',
            'last_name': 'last'
        }
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), initial_users + 1)
        self.assertTrue(User.objects.filter(username='test_user').exists())

        messages = list(get_messages(response.wsgi_request))
        assert "успешно" in str(messages[0]).lower()

    def test_unauthenticated_access(self):
        available_actions = ['update', 'delete']
        for action in available_actions:
            url = reverse(f'users:{action}', kwargs={'pk': self.user.pk})
            response = self.client.post(url)

            login_url = reverse('login')
            expected_redirect = f"{login_url}"
            self.assertRedirects(response, expected_redirect)

            messages = list(get_messages(response.wsgi_request))
            assert "не авторизованы" in str(messages[0]).lower()

    def test_update_authenticated(self):
        self.client.login(username='user1', password=TEST_PASSWORD)
        url = reverse('users:update', kwargs={'pk': self.user.pk})
        response = self.client.post(
            url,
            {
                'username': 'user1',
                'first_name': 'last',
                'last_name': 'first',
                'password1': '!!!87654321',
                'password2': '!!!87654321',
            }
        )
        self.assertRedirects(response, reverse('users:index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'last')
        self.assertTrue(self.user.check_password('!!!87654321'))
    
    def test_delete_authenticated(self):
        self.client.login(username='user1', password=TEST_PASSWORD)
        url = reverse('users:delete', kwargs={'pk': self.user.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users:index'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_cannot_delete_user_with_tasks(self):
        status = Status.objects.create(name='В работе')

        Task.objects.create(
            name="Test task",
            status=status,
            author=self.user
        )

        self.client.login(username='user1', password=TEST_PASSWORD)
        self.client.post(reverse('users:delete', args=[self.user.pk]))

        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())


