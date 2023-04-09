from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)

class Special(models.Model):
    name = models.CharField(max_length=255, verbose_name='Специальность')


class Employee(models.Model):
    fio = models.CharField(max_length=255)
    specail = models.ManyToManyField(Special, blank=True, null=True, related_name='employees')
    medical_center = models.ForeignKey('MedicalCenter', blank=True, null=True, related_name='employees',
                                       on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

class MedicalCenter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя центра')
    address = models.CharField(max_length=255, verbose_name='Адрес центра')
    city = models.ManyToManyField(City, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RegisterRequest(models.Model):
    phone = models.CharField(max_length=255)
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    medical_center = models.ForeignKey(MedicalCenter, blank=True, null=True, related_name='register_request',
                                       on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, related_name='register_request', on_delete=models.CASCADE)
    special = models.ForeignKey(Special, blank=True, null=True, on_delete=models.CASCADE, related_name='register_request')
    register_at = models.DateField(auto_now_add=False)
    created_at = models.DateField(auto_now=True)

