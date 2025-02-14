import uuid
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_inscode import mixins
from django_inscode.serializers import Serializer
from django_inscode.views import ModelView, GenericModelView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from comum.models import CarModel, Part
from comum.services import car_model_service
from comum.transports import CarModelTransport, PartsToRemoveTransport

class CarModelView(ModelView, PermissionRequiredMixin):

    fields = {
        "name",
        "manufacturer",
        "year"
    }

    paginate_by = 10
    service = car_model_service
    serializer = Serializer(CarModel, CarModelTransport)
    lookup_field = "car_model_id"

    permission_map = {
        'GET': 'comum.view_carmodel',
        'POST': 'comum.add_carmodel',
        'DELETE': 'comum.delete_carmodel',
        'PATCH': 'comum.change_carmodel',
        'PUT': 'comum.change_carmodel',
    }

    def get_context(self, request):
        return {

        }

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

class CarsModelPartView(GenericModelView, mixins.ViewRetrieveModelMixin):

    service = car_model_service
    serializer = Serializer(CarModel, CarModelTransport)
    lookup_field = "car_model_id"

    permission_map = {
        'GET': 'comum.view_carmodel',
    }

    def get_queryset(self, filter_kwargs=None):
        queryset = super().get_queryset(filter_kwargs)
        part_id = self.kwargs.get('part_id')
        queryset = queryset.filter(parts__id=part_id)
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

class RemovePartsCarModelView(GenericModelView, mixins.ViewUpdateModelMixin):

    service = car_model_service
    serializer = Serializer(CarModel, PartsToRemoveTransport)
    lookup_field = "car_model_id"
    permission_map = {
        'DELETE': 'comum.delete_carmodel',
    }

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

    def _update(self, request: HttpRequest, *args, **kwargs):
        car_model = self.get_object()
        data = self.parse_request_data(request)
        ids = data.get('part_ids', [])
        parts_removed_count = 0
        invalid_part_ids = []
        removed_part_ids = []

        if not isinstance(ids, list):
            return JsonResponse({"detail": "O campo 'part_ids' deve ser uma lista."}, status=status.HTTP_400_BAD_REQUEST)

        for part_id_str in ids:
            try:
                part_id = uuid.UUID(part_id_str)
                if car_model.parts.filter(pk=part_id).exists():
                    part = Part.objects.get(pk=part_id)
                    car_model.parts.remove(part)
                    parts_removed_count += 1
                    removed_part_ids.append(part_id_str)
                else:
                    invalid_part_ids.append(part_id_str)
            except (ValueError, TypeError):
                invalid_part_ids.append(part_id_str)
            except Part.DoesNotExist:
                invalid_part_ids.append(part_id_str)

        car_model.save()

        if parts_removed_count > 0 or invalid_part_ids:
            response_data = {
                "detail": f"{parts_removed_count} peças removidas.",
                "removed_part_ids": removed_part_ids,
                "invalid_part_ids": invalid_part_ids
            }

            status_code = status.HTTP_200_OK if invalid_part_ids else status.HTTP_204_NO_CONTENT
            return JsonResponse(response_data, status=status_code)

        return JsonResponse({"detail": "Nenhuma peça foi removida."}, status=status.HTTP_200_OK)


class AssociatePartsToCarModelsView(APIView):

    def post(self, request):
        car_model_ids = request.data.get('car_model_ids')
        part_ids = request.data.get('part_ids')

        if not car_model_ids:
            return JsonResponse({'error': 'car_model_ids é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        if not part_ids:
            return JsonResponse({'error': 'part_ids é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(car_model_ids, list):
            return JsonResponse({'error': 'car_model_ids deve ser uma lista'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(part_ids, list):
            return JsonResponse({'error': 'part_ids deve ser uma lista'}, status=status.HTTP_400_BAD_REQUEST)

        associated_parts = {}
        not_found_parts = {}
        not_found_car_models = []

        for car_model_id in car_model_ids:
            try:
                car_model = CarModel.objects.get(pk=car_model_id)
                associated_parts[car_model_id] = []
                not_found_parts[car_model_id] = []

                for part_id in part_ids:
                    try:
                        part = Part.objects.get(pk=part_id)
                        car_model.parts.add(part)
                        associated_parts[car_model_id].append(part_id)
                    except Part.DoesNotExist:
                        not_found_parts[car_model_id].append(part_id)

                car_model.save()

            except CarModel.DoesNotExist:
                not_found_car_models.append(car_model_id)

        if associated_parts:
            message = {'message': 'Peças associadas com sucesso', 'associated_parts': associated_parts}
            if not_found_parts:
                message['not_found_parts'] = not_found_parts
            if not_found_car_models:
                message['not_found_car_models'] = not_found_car_models
            return JsonResponse(message, status=status.HTTP_200_OK)
        else:
            message = {'error': 'Nenhum modelo de carro ou peça encontrada para associar'}
            if not_found_car_models:
                message['not_found_car_models'] = not_found_car_models
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)