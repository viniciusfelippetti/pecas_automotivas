from django_inscode.services import ModelService

from comum.base_service import BaseService
from comum.repositories import user_repository
from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest

from django_inscode import exceptions

from typing import Dict, Optional, Any


class AuthService(BaseService):
    def __init__(self, user_repository):
        super().__init__(user_repository)

    def sign_in(
        self,
        request: HttpRequest,
        password: str,
        username: Optional[str],
        email: Optional[str],
    ) -> Dict[str, Any]:
        if email is not None and username is not None:
            raise exceptions.UnprocessableEntity(
                errors={"username": "Forneça apenas 'username' ou 'email' de uma vez."}
            )

        if email is not None:
            user = authenticate(request, email=email, password=password)

        if username is not None:
            user = authenticate(request, username=username, password=password)

        if user is None:
            raise exceptions.Unauthorized(
                errors={"invalid_authentication": "Email/Username ou senha inválidos."}
            )

        login(request, user)


        return {
            "user": user,
            "session_id": request.session.session_key,
        }

    def sign_out(self, request: HttpRequest) -> None:
        logout(request)


auth_service = AuthService(user_repository)