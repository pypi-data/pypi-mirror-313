from typing import *
import pytest
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import APIClient

from wcd_2factor.models import MethodConfig, UserConfig, ConfirmationState


@pytest.mark.django_db
def test_user_config_creation_unauthenticated():
    api_client = APIClient()
    response = api_client.post('/test/user-config/own/create/')

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_config_creation_pipeline():
    api_client = APIClient()
    user = User.objects.create_user(username='test', password='test')
    api_client.force_authenticate(user)
    active = MethodConfig.objects.create(method='dummy', is_active=True)

    response = api_client.post('/test/user-config/own/create/', {
        'method_config_id': active.pk,
        'config': {}, 'is_active': False, 'is_default': False,
    }, format='json')

    assert response.status_code == 400
    assert 'code' in response.data['config']

    # Creating user config
    response = api_client.post('/test/user-config/own/create/', {
        'method_config_id': active.pk,
        'config': {'code': 'some'}, 'is_active': False, 'is_default': False,
    }, format='json')

    assert response.status_code == 200

    item = response.data['item']
    id = item['id']
    confirmation_id = response.data['comfirmation_id']

    assert confirmation_id is not None
    assert item['config']['code'] == 'some'
    assert UserConfig.objects.filter(pk=id, user=user).exists()

    # Can't confirm, because of unconfirmed user config
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'some'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['id'][0].code == 'wrong_config'

    # Should confirm user config using specialized method
    # Wrong attempts first:
    response = api_client.post('/test/user-config/own/confirm/', {
        'id': id,
        'confirmation_id': confirmation_id,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['non_field_errors'][0].code == 'failed_to_confirm'

    response = api_client.post('/test/user-config/own/confirm/', {
        'id': id,
        'confirmation_id': confirmation_id,
        'data': {'code': 'some'},
    }, format='json')

    assert response.status_code == 200
    assert response.data['status'] == UserConfig.Status.CONFIRMED

    assert UserConfig.objects.filter(
        pk=id, user=user, status=UserConfig.Status.CONFIRMED
    ).exists()

    # Updating user config without confirmation
    # Activating for example.
    response = api_client.put(f'/test/user-config/own/{id}/update/', {
        'config': {'code': 'some'}, 'is_active': True, 'is_default': False,
    }, format='json')

    assert response.status_code == 200
    assert response.data['item']['status'] == UserConfig.Status.CONFIRMED
    assert response.data['comfirmation_id'] is None

    response = api_client.put(f'/test/user-config/own/{id}/update/', {
        'config': {'code': 'new'}, 'is_active': True, 'is_default': False,
    }, format='json')

    assert response.status_code == 200
    assert response.data['item']['status'] == UserConfig.Status.IN_PROCESS
    assert response.data['comfirmation_id'] is not None

    # Destroying user config
    response = api_client.delete(f'/test/user-config/own/{id}/destroy/')

    assert response.status_code == 204
