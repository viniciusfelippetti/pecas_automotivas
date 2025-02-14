import random
from decimal import Decimal
import factory
from comum.models import Part
import uuid

class PartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Part

    id = factory.LazyFunction(uuid.uuid4)
    part_number = factory.Faker("part_number")
    name = factory.Faker("name")
    details = factory.Faker("details")
    price = factory.LazyFunction(lambda: round(Decimal(random.randrange(10000)) / 100,2))
    quantity = factory.LazyFunction(lambda: random.randrange(1, 100))