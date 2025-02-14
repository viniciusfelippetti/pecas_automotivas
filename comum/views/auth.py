from comum.services import auth_service, user_service
from django.views import View
from django.http import HttpRequest, JsonResponse
from comum.transports.user import UserTransport
import json

from comum.utils.serializer import serializer


class SignUpView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)
        user = user_service.perform_action("create", data=data, context={})
        return JsonResponse(
            serializer(user, UserTransport),
            status=201,
        )


class SignInView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body)
        sign_in_data = auth_service.sign_in(
            request,
            password=data.get("password"),
            username=data.get("username"),
            email=data.get("email"),
        )

        return JsonResponse(
            {
                **serializer(sign_in_data["user"], UserTransport),
                "session_id": sign_in_data["session_id"],
            },
            status=201,
        )


class SignOutView(View):
    def post(self, request):
        auth_service.sign_out(request)
        return JsonResponse(data={}, status=200)
