from typing import *
import pytest
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.test import APIClient

from wcd_2factor.models import MethodConfig, UserConfig, ConfirmationState


@pytest.mark.django_db
def test_method_confirmation_pipeline():
    api_client = APIClient()
    active = MethodConfig.objects.create(method='dummy', is_active=True)

    # Wrong request attempt
    response = api_client.post('/test/confirmation/request/', {
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['non_field_errors'][0].code == 'empty_config'

    response = api_client.post('/test/confirmation/request/', {
        'method_config_id': active.pk,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 200
    assert not response.data['is_available']

    confirmation_id = response.data['id']

    # Wrong confirmation attempt
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['non_field_errors'][0].code == 'failed_to_confirm'

    # Successfull confirmation
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'dummy-method'},
    }, format='json')

    assert response.status_code == 200
    assert response.data['status'] == ConfirmationState.Status.CONFIRMED

    # Confirmed confirmation state confirmation attempt
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'some'},
    }, format='json')

    assert response.status_code == 400
    assert 'id' in response.data

    # Checking confirmation state
    response = api_client.get(f'/test/confirmation/{confirmation_id}/check/')

    assert response.status_code == 200
    assert response.data['status'] == ConfirmationState.Status.CONFIRMED
    assert response.data['is_available']


@pytest.mark.django_db
def test_user_config_confirmation_pipeline():
    api_client = APIClient()
    user = User.objects.create_user(username='test', password='test')
    api_client.force_authenticate(user)
    active = MethodConfig.objects.create(method='dummy', is_active=True)
    different_active = MethodConfig.objects.create(method='dummy', is_active=True)
    user_active = UserConfig.objects.create(
        method_config=active, is_active=True, status=UserConfig.Status.CONFIRMED,
        user=user, config={'code': 'dummy-user'},
    )

    # Wrong request attempt
    response = api_client.post('/test/confirmation/request/', {
        'method_config_id': different_active.pk,
        'user_config_id': user_active.pk,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['non_field_errors'][0].code == 'invalid'

    response = api_client.post('/test/confirmation/request/', {
        'method_config_id': active.pk,
        'user_config_id': user_active.pk,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 200
    assert not response.data['is_available']

    response = api_client.post('/test/confirmation/request/', {
        'user_config_id': user_active.pk,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 200
    assert not response.data['is_available']

    confirmation_id = response.data['id']

    # Wrong confirmation attempt
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'wrong'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['non_field_errors'][0].code == 'failed_to_confirm'

    # Truying to confirm using method, not user config
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'dummy-method'},
    }, format='json')

    assert response.status_code == 400
    assert response.data['non_field_errors'][0].code == 'failed_to_confirm'

    # Successfull confirmation
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'dummy-user'},
    }, format='json')

    assert response.status_code == 200
    assert response.data['status'] == ConfirmationState.Status.CONFIRMED

    # Confirmed confirmation state confirmation attempt
    response = api_client.post('/test/confirmation/confirm/', {
        'id': confirmation_id,
        'data': {'code': 'some'},
    }, format='json')

    assert response.status_code == 400
    assert 'id' in response.data

    # Checking confirmation state
    response = api_client.get(f'/test/confirmation/{confirmation_id}/check/')

    assert response.status_code == 200
    assert response.data['status'] == ConfirmationState.Status.CONFIRMED
    assert response.data['is_available']
