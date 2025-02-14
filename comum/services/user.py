from django_inscode.services import ModelService
from django_inscode import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from comum.repositories import user_repository

class UserService(ModelService):
    def validate(self, data, instance=None):
        errors = {}

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password and confirm_password is None:
            raise exceptions.BadRequest(errors={"confirm_password": "Campo ausente."})

        if password and confirm_password and password != confirm_password:
            errors["password"] = "As senhas devem ser iguais."

        if errors:
            raise exceptions.UnprocessableEntity(errors=errors)

        if password and confirm_password:
            try:
                validate_password(password, instance)
            except ValidationError as e:
                errors["password"] = e.messages

        if errors:
            raise exceptions.UnprocessableEntity(errors=errors)

    def create(self, data, context):
        email = data.get("email")
        password = data.get("password")

        del data["confirm_password"]

        data["password"] = make_password(password)
        data["email"] = BaseUserManager.normalize_email(email)
        print(data)
        return super().create(data, context)

    def update(self, id, data, context):
        password = data.get("password")

        if password:
            data["password"] = make_password(password)

        return super().update(id, data, context)


user_service = UserService(user_repository)