from django.db import models
from django_inscode.models import SoftDeleteBaseModel



class CarModel(SoftDeleteBaseModel):
    name = models.CharField(max_length=60)
    manufacturer = models.CharField(max_length=60)
    year = models.IntegerField()
    parts = models.ManyToManyField("Part", blank=True, related_name='parts')
   
   
    class Meta:
        verbose_name = "Car model"
        verbose_name_plural = "Car models"