from django.db import models
from django_inscode.models import SoftDeleteBaseModel


class Part(SoftDeleteBaseModel):
    part_number = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    details = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Part"
        verbose_name_plural = "Parts"