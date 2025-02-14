from django.contrib.auth.models import Group
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_inscode.views import GenericModelView
from django_inscode.serializers import Serializer
from django_inscode import mixins
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from comum.services import user_service
from comum.transports import UserTransport
from comum.models import Users
from comum.transports.user import AddUserGroupTransport


class UserView(
    mixins.ViewRetrieveModelMixin,
    mixins.ViewUpdateModelMixin,
    mixins.ViewDeleteModelMixin,
    GenericModelView,
):
    permissions_required = {
        "get": {"VIEW_USER"},
        "patch": {"EDIT_USER"},
        "delete": {"DELETE_USER"},
    }
    lookup_field = "user_id"
    serializer = Serializer(Users, UserTransport)
    service = user_service

    def has_permission(self):
        user_id = self.request.resolver_match.kwargs.get("user_id")

        if str(user_id) == str(self.request.user.id):
            return True

        return super().has_permission()


class AddUserGroupModelView(GenericModelView, mixins.ViewUpdateModelMixin):

    service = user_service
    serializer = Serializer(Users, AddUserGroupTransport)
    lookup_field = "user_id"
    permission_map = {
        'PATCH': 'comum.change_user',
    }

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        self._check_jwt_authentication(self.request)
        return super().dispatch(*args, **kwargs)

    def _check_jwt_authentication(self, request):
        """ Verifica a autenticação JWT manualmente. """
        auth = request.headers.get('Authorization')

        if not auth:
            raise AuthenticationFailed('No Authorization header provided.')

        try:
            token = auth.split(' ')[1]

            JWTAuthentication().authenticate(request)
        except (IndexError, ValueError):
            raise AuthenticationFailed('Invalid token format.')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

        if not request.user.is_authenticated:
            raise AuthenticationFailed('User is not logged in.')

    def _update(self, request: HttpRequest, *args, **kwargs):
        user = self.get_object()
        data = self.parse_request_data(request)
        ids = data.get('group_ids', [])
        groups_add_count = 0
        invalid_group_ids = []
        add_group_ids = []

        if not isinstance(ids, list):
            return JsonResponse({"detail": "O campo 'group_-ids' deve ser uma lista."}, status=status.HTTP_400_BAD_REQUEST)

        for group_id in ids:
            try:
                if user.groups.filter(pk=group_id).exists():
                    group = Group.objects.get(pk=group_id)
                    user.groups.add(group)
                    groups_add_count += 1
                    add_group_ids.append(group_id)
                else:
                    invalid_group_ids.append(group_id)
            except (ValueError, TypeError):
                invalid_group_ids.append(group_id)
            except Group.DoesNotExist:
                invalid_group_ids.append(group_id)

        user.save()

        if groups_add_count > 0 or invalid_group_ids:
            response_data = {
                "detail": f"{groups_add_count} grupos vinculados.",
                "add_group_ids": add_group_ids,
                "invalid_group_ids": invalid_group_ids
            }

            status_code = status.HTTP_200_OK if invalid_group_ids else status.HTTP_204_NO_CONTENT
            return JsonResponse(response_data, status=status_code)

        return JsonResponse({"detail": "Nenhum grupo foi vinculado."}, status=status.HTTP_200_OK)