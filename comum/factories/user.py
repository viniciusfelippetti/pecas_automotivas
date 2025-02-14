import factory
from comum.models import Users
import uuid


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users
        django_get_or_create = ["email", "username"]

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Faker("email")
    username = factory.Faker("user_name")
    is_active = True
    is_staff = False
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")