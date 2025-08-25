import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Status

User = get_user_model()


@pytest.mark.django_db
class TestStatus:
    @pytest.fixture
    def logged_client(self, client):
        username = 'user1'
        password = 'letmeinplease'
        User.objects.create_user(username=username,
                                 password=password)
        client.login(username=username, password=password)
        return client

    def test_create(self, logged_client):
        status_name = 'В работе'
        url = reverse('statuses:create')
        response = logged_client.post(url, {'name': status_name})
        assert response.status_code == 302
        assert Status.objects.filter(name=status_name).exists()

    def test_update(self, logged_client):
        status = Status.objects.create(name='В работе')
        new_name = 'Завершён'
        url = reverse('statuses:update', args=[status.pk])
        logged_client.post(url, {'name': new_name})
        status.refresh_from_db()
        assert status.name == new_name

    def test_delete(self, logged_client):
        status = Status.objects.create(name='В работе')
        url = reverse('statuses:delete', args=[status.pk])
        logged_client.post(url)
        assert not Status.objects.filter(pk=status.pk).exists()

    def test_auth_required(self, client):
        url = reverse('statuses:index')
        response = client.get(url)
        assert response.status_code == 302
