from typing import *
import pytest
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import APIClient

from wcd_2factor.models import MethodConfig, UserConfig


@pytest.mark.django_db
def test_method_config_list(client):
    response = client.get('/test/method-config/list/active/')

    assert response.status_code == 200
    assert response.data == []

    active = MethodConfig.objects.create(method='dummy', is_active=True)
    inactive = MethodConfig.objects.create(method='dummy', is_active=False)

    response2 = client.get('/test/method-config/list/active/')

    assert response2.status_code == 200
    assert len(response2.data) == 1
    item, = response2.data
    assert item['id'] == active.id
    assert item['method'] == 'dummy'
    assert item['is_default'] == False


@pytest.mark.django_db
def test_user_config_list():
    api_client = APIClient()
    response = api_client.get('/test/user-config/own/list/')

    assert response.status_code == 403

    user1 = User.objects.create_user(username='test', password='test')
    user2 = User.objects.create_user(username='test2', password='test')

    api_client.force_authenticate(user1)

    response2 = api_client.get('/test/user-config/own/list/')

    assert response2.status_code == 200
    assert len(response2.data) == 0

    active = MethodConfig.objects.create(method='dummy', is_active=True)
    inactive = MethodConfig.objects.create(method='dummy', is_active=False)

    user1_active, user1_inactive, *_, user2_confirmed = UserConfig.objects.bulk_create([
        UserConfig(user=user1, method_config=active, is_active=True),
        UserConfig(user=user1, method_config=active, is_active=False),
        UserConfig(user=user1, method_config=inactive, is_active=True),
        UserConfig(user=user1, method_config=inactive, is_active=False),

        UserConfig(
            user=user2, method_config=active,
            is_active=True, status=UserConfig.Status.CONFIRMED,
        ),
    ])

    response2 = api_client.get('/test/user-config/own/list/')

    assert response2.status_code == 200
    assert len(response2.data) == 2

    item1, item2 = response2.data
    assert item1['id'] == user1_active.id
    assert item1['method_config']['id'] == active.id
    assert item1['is_active'] == True
    assert item2['is_available'] == False

    assert item2['id'] == user1_inactive.id
    assert item2['method_config']['id'] == active.id
    assert item2['is_active'] == False
    assert item2['is_available'] == False

    api_client.force_authenticate(user2)

    response3 = api_client.get('/test/user-config/own/list/')

    assert response3.status_code == 200
    assert len(response3.data) == 1

    item1, = response3.data
    assert item1['id'] == user2_confirmed.id
    assert item1['method_config']['id'] == active.id
    assert item1['is_active'] == True
    assert item1['is_available'] == True
