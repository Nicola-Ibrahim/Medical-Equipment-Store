from django.db import models
from accounts.models import Warehouse

class WarehouseProfile(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='details', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    working_hours = models.FloatField()
    sections = models.IntegerField()
    profit_percentage = models.FloatField()