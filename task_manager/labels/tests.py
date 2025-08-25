import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()

TEST_PASSWORD = 'letmeinplease'


@pytest.mark.django_db
class TestLabelViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password=TEST_PASSWORD,
        )
        self.label = Label.objects.create(name='label')
        self.status = Status.objects.create(name='status')
        self.client.login(username='user1', password=TEST_PASSWORD)

    def test_label_list_view(self):
        response = self.client.get(reverse('labels:index'))
        assert response.status_code == 200
        assert 'label' in response.content.decode()

    def test_create(self):
        response = self.client.post(
                reverse('labels:create'),
                {'name': 'success'},
            )
        assert response.status_code == 302
        assert Label.objects.filter(name='success').exists()

    def test_update(self):
        response = self.client.post(
                reverse('labels:update',
                args=[self.label.id]),
                {'name': 'newname'},
            )
        assert response.status_code == 302
        self.label.refresh_from_db()
        assert self.label.name == 'newname'

    def test_delete(self):
        response = self.client.post(reverse('labels:delete',
                                            args=[self.label.id]))
        assert response.status_code == 302
        assert not Label.objects.filter(id=self.label.id).exists()

    def test_delete_used_label(self):
        task = Task.objects.create(name='finish project', author=self.user,
                                   status=self.status)
        task.labels.add(self.label)

        response = self.client.post(reverse('labels:delete',
                                            args=[self.label.id]))
        assert response.status_code == 302
        assert Label.objects.filter(pk=self.label.pk).exists()