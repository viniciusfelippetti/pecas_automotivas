import factory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from comum.models import CarModel, Part


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    codename = factory.Sequence(lambda n: f"permissao_{n}")
    name = factory.LazyAttribute(lambda o: o.codename.replace("_", " ").title())
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(
            CarModel) if "carmodel" in o.codename else ContentType.objects.get_for_model(Part)
    )