from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_inscode import mixins
from django_inscode.serializers import Serializer
from django_inscode.views import ModelView, GenericModelView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from comum.models import Part
from comum.services import part_service
from comum.transports import PartTransport


class PartView(ModelView):

    fields = {
        "part_number",
        "name",
        "details",
        "price",
        "quantity"
    }

    paginate_by = 10
    service = part_service
    serializer = Serializer(Part, PartTransport)
    lookup_field = "part_id"

    permission_map = {
        'GET': 'comum.view_part',
        'POST': 'comum.add_part',
        'DELETE': 'comum.delete_part',
        'PATCH': 'comum.change_part',
        'PUT': 'comum.change_part',
    }

    def get_context(self, request):
        return {"user": request.user}

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        self._check_jwt_authentication(self.request)
        if self.request.user.is_authenticated:
            self._check_permission(self.request, self.request.method)
        return super().dispatch(*args, **kwargs)

    def _check_permission(self, request: HttpRequest, method: str):
        """
        Verifica se o usuário tem a permissão necessária para o método HTTP.
        """
        required_permission = self.permission_map.get(method)
        if required_permission:
            if not request.user.has_perm(required_permission):
                raise PermissionDenied(
                    f"Você não tem permissão para realizar esta ação.")

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


class PartsCarModelView(GenericModelView, mixins.ViewRetrieveModelMixin):

    service = part_service
    serializer = Serializer(Part, PartTransport)
    lookup_field = "part_id"

    permission_map = {
        'GET': 'comum.view_part',
    }

    def get_queryset(self, filter_kwargs=None):
        queryset = super().get_queryset(filter_kwargs)
        car_model_id = self.kwargs.get('car_model_id')
        queryset = queryset.filter(parts__id=car_model_id)
        return queryset

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        self._check_jwt_authentication(self.request)
        if self.request.user.is_authenticated:
            self._check_permission(self.request, self.request.method)
        return super().dispatch(*args, **kwargs)

    def _check_permission(self, request: HttpRequest, method: str):
        """
        Verifica se o usuário tem a permissão necessária para o método HTTP.
        """
        required_permission = self.permission_map.get(method)
        if required_permission:
            if not request.user.has_perm(required_permission):
                raise PermissionDenied(
                    f"Você não tem permissão para realizar esta ação.")

    def _check_jwt_authentication(self, request):
        """ Verifica a autenticação JWT manualmente. """
        print(request.user)
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