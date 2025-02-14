import os
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from rest_framework import views, parsers, status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from comum.tasks import process_csv_upload

class CSVUploadView(generics.GenericAPIView, PermissionRequiredMixin):

    parser_classes = [parsers.MultiPartParser]
    permission_map = {
        'POST': 'comum.add_part',
    }

    def _check_permission(self, request: HttpRequest, method: str):
        """
        Verifica se o usuário tem a permissão necessária para o método HTTP.
        """
        required_permission = self.permission_map.get(method)
        if required_permission:
            if not request.user.has_perm(required_permission):
                raise PermissionDenied(
                    f"Você não tem permissão para realizar esta ação.")

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self._check_permission(self.request, self.request.method)

        file_obj = request.FILES['file']
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        with open(f'temp/{file_obj.name}', 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        process_csv_upload.delay(f'temp/{file_obj.name}')

        return Response({"message": "Arquivo CSV enviado para processamento."}, status=status.HTTP_202_ACCEPTED)