from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView,
)
from rest_framework import permissions, status, response

from wcd_2factor.confirmer import default_confirmer
from wcd_2factor.models import ConfirmationState

from .serializers import (
    ConfirmationStateDisplaySerializer,
    MethodConfigDisplaySerializer,
    UserConfigDisplaySerializer, UserConfigCreateSerializer,
    UserConfigUpdateSerializer, UserConfigConfirmSerializer,
    ConfirmSerializer, ConfirmationRequestSerializer,
)


__all__ = (
    'MethodConfigListActive',
    'UserConfigOwnList', 'UserConfigOwnCreate', 'UserConfigOwnDestroy',
    'ConfirmationConfirm',
    'user_config_own_list_view', 'method_config_list_active_view',
    'make_urlpatterns',
)


class MethodConfigListActive(ListAPIView):
    serializer_class = MethodConfigDisplaySerializer

    def get_queryset(self):
        return default_confirmer.get_method_configs()


class UserConfigOwnMixin:
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            default_confirmer
            .get_user_configs(user=self.request.user)
            .select_related('method_config')
        )


class UserConfigOwnList(UserConfigOwnMixin, ListAPIView):
    serializer_class = UserConfigDisplaySerializer


class RespondWithConfirmationMixin:
    def render_to_response(self, serializer):
        return response.Response(
            {
                'item': serializer.data,
                'comfirmation_id': (
                    serializer.confirmation.pk
                    if serializer.confirmation is not None else
                    None
                ),
            },
            status=status.HTTP_200_OK,
        )


class UserConfigOwnCreate(RespondWithConfirmationMixin, UserConfigOwnMixin, CreateAPIView):
    serializer_class = UserConfigCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return self.render_to_response(serializer)


class UserConfigOwnUpdate(RespondWithConfirmationMixin, UserConfigOwnMixin, UpdateAPIView):
    serializer_class = UserConfigUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.render_to_response(serializer)


class UserConfigOwnConfirm(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserConfigConfirmSerializer(
            data=request.data, context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        user_config = serializer.commit()

        return response.Response(
            UserConfigDisplaySerializer(instance=user_config).data,
            status=status.HTTP_200_OK,
        )


class UserConfigOwnDestroy(UserConfigOwnMixin, DestroyAPIView):
    pass


class ConfirmationRequest(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ConfirmationRequestSerializer(
            data=request.data, context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        confirmation = serializer.commit()

        return response.Response(
            ConfirmationStateDisplaySerializer(instance=confirmation).data,
            status=status.HTTP_200_OK,
        )


class ConfirmationConfirm(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ConfirmSerializer(
            data=request.data, context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        confirmation = serializer.commit()

        return response.Response(
            ConfirmationStateDisplaySerializer(instance=confirmation).data,
            status=status.HTTP_200_OK,
        )


class ConfirmationCheck(GenericAPIView):
    queryset = ConfirmationState.objects.all()

    def get(self, request, *args, pk, **kwargs):
        available, confirmation = default_confirmer.check(
            id=pk, context=self.get_serializer_context(),
        )

        return response.Response({
            'id': confirmation.pk if confirmation is not None else None,
            'status': confirmation.status if confirmation is not None else None,
            'is_available': available,
        }, status=status.HTTP_200_OK)


method_config_list_active_view = MethodConfigListActive.as_view()

user_config_own_list_view = UserConfigOwnList.as_view()
user_config_own_create_view = UserConfigOwnCreate.as_view()
user_config_own_update_view = UserConfigOwnUpdate.as_view()
user_config_own_confirm_view = UserConfigOwnConfirm.as_view()
user_config_own_destroy_view = UserConfigOwnDestroy.as_view()

confirmation_request_view = ConfirmationRequest.as_view()
confirmation_confirm_view = ConfirmationConfirm.as_view()
confirmation_check_view = ConfirmationCheck.as_view()


def make_urlpatterns(
    method_config_list_active=method_config_list_active_view,

    user_config_own_list=user_config_own_list_view,
    user_config_own_create=user_config_own_create_view,
    user_config_own_update=user_config_own_update_view,
    user_config_own_confirm=user_config_own_confirm_view,
    user_config_own_destroy=user_config_own_destroy_view,

    confirmation_request=confirmation_request_view,
    confirmation_confirm=confirmation_confirm_view,
    confirmation_check=confirmation_check_view,
):
    return [
        path('method-config/', include(([
            path('list/', include(([
                path('active/', csrf_exempt(method_config_list_active), name='active'),
            ], 'list'))),
        ], 'method-config'))),
        path('user-config/', include(([
            path('own/', include(([
                path('list/', user_config_own_list, name='list'),
                path('create/', user_config_own_create, name='create'),
                path('confirm/', user_config_own_confirm, name='confirm'),
                path('<int:pk>/update/', user_config_own_update, name='update'),
                path('<int:pk>/destroy/', user_config_own_destroy, name='destroy'),
            ], 'own'))),
        ], 'user-config'))),
        path('confirmation/', include(([
            path('request/', csrf_exempt(confirmation_request), name='request'),
            path('confirm/', csrf_exempt(confirmation_confirm), name='confirm'),
            path('<str:pk>/check/', csrf_exempt(confirmation_check), name='check'),
        ], 'confirmation'))),
    ]
