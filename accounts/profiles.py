from django.db import models
from accounts.models import *



#################
## Accountants ###
#################
class BaseAccountantProfile(models.Model):
    base_accountant = models.OneToOneField(BaseAccountant, related_name='base_accountant_details', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    

    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name

class DeliveryWorkerAccountantProfile(models.Model):
    delivery_worker_accountant = models.OneToOneField(DeliveryWorkerAccountant, related_name='delivery_worker_accountant_details', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    

    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name


class WarehouseAccountantProfile(models.Model):
    warehouse_accountant = models.OneToOneField(WarehouseAccountant, related_name='warehouse_accountant_details', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    

    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name

class WarehouseProfile(models.Model):
    warehouse = models.OneToOneField(Warehouse, related_name='warehouse_details', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    service = models.CharField(max_length=200)
    working_hours = models.FloatField()
    sections = models.IntegerField()
    profit_percentage = models.FloatField()



class DeliveryWorkerProfile(models.Model):
    delivery_worker = models.OneToOneField(DeliveryWorker, related_name='delivery_worker_details', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    distance = models.FloatField(max_length=200)
    duration = models.FloatField()
    profit_percentage = models.FloatField()

    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name


class DoctorProfile(models.Model):
    doctor = models.OneToOneField(Doctor, related_name='doctor_details', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name


class DoctorProfile(models.Model):
    delivery_worker = models.OneToOneField(Doctor, related_name='doctor_details', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name