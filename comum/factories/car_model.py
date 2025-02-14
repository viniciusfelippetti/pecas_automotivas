import random
import factory
from comum.models import CarModel
import uuid

class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    manufacturer = factory.Faker("manufacturer")
    year = factory.LazyFunction(lambda: random.randrange(2000, 2025))