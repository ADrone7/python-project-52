import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()

TEST_PASSWORD = 'letmeinplease'


@pytest.mark.django_db
class TasksTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='author',
            password=TEST_PASSWORD
        )
        self.user2 = User.objects.create_user(
            username='executor',
            password=TEST_PASSWORD
        )
        self.status = Status.objects.create(name='В работе')

    def test_create(self):
        self.client.login(username='author', password=TEST_PASSWORD)
        url = reverse('tasks:create')
        data = {
            'name': 'Сделать рефакторинг',
            'description': 'Этот код ужасен',
            'status': self.status.id,
            'executor': self.user2.id,
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        assert Task.objects.count() == 1
        assert Task.objects.first().author == self.user1

    def test_delete_by_non_author(self):
        task = Task.objects.create(
            name='Править тесты',
            status=self.status,
            author=self.user1,
        )
        self.client.login(username='executor', password=TEST_PASSWORD)
        url = reverse('tasks:delete', kwargs={'pk': task.id})
        response = self.client.post(url)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        assert str(messages[0]) == "Задачу может удалить только ее автор"

    def test_delete_by_author(self):
        task = Task.objects.create(
            name='Писать тесты',
            status=self.status,
            author=self.user1,
        )
        self.client.login(username='author', password=TEST_PASSWORD)
        url = reverse('tasks:delete', kwargs={'pk': task.id})
        response = self.client.post(url)
        assert response.status_code == 302
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_update(self):
        task = Task.objects.create(
            name='Задеплоить проект',
            status=self.status,
            author=self.user1,
        )
        new_name = 'Пить чай'
        self.client.login(username='executor', password=TEST_PASSWORD)
        url = reverse('tasks:update', kwargs={'pk': task.id})
        response = self.client.post(url, {
            'name': new_name,
            'description': 'С печеньками',
            'status': self.status.id
        })
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.name == new_name

    def test_filter_by_executor(self):
        Task.objects.create(
            name='Задеплоить проект1',
            status=self.status,
            author=self.user1,
            executor=self.user2,
        )
        Task.objects.create(
            name='Задеплоить проект2',
            status=self.status,
            author=self.user2,
            executor=self.user1,
        )
        self.client.login(username='executor', password=TEST_PASSWORD)
        url = reverse('tasks:index')
        response = self.client.get(url, {
            'executor': self.user1.pk,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задеплоить проект2')
        self.assertNotContains(response, 'Задеплоить проект1')

    def test_filter_self_tasks(self):
        Task.objects.create(
            name='Задеплоить проект1',
            status=self.status,
            author=self.user1,
            executor=self.user2,
        )
        Task.objects.create(
            name='Задеплоить проект2',
            status=self.status,
            author=self.user2,
            executor=self.user1,
        )
        self.client.login(username='author', password=TEST_PASSWORD)
        url = reverse('tasks:index')
        response = self.client.get(url, {
            'self_tasks': 'on',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задеплоить проект1')
        self.assertNotContains(response, 'Задеплоить проект2')