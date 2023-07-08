from django.contrib.auth.models import User as Account
from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, primary_key=True)
    id = models.CharField(max_length=30)
    id_type = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    cellphone = models.CharField(max_length=20)


class Patient(models.Model):
    patient_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cellphone = models.CharField(max_length=20, default="0")
    blood_type = models.CharField(max_length=10)
    actual_estimation = models.FloatField(default=0)


class MedicPatient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Results(models.Model):
    result_id = models.AutoField(primary_key=True)
    date = models.DateField()
    age = models.IntegerField()
    sex = models.CharField(max_length=2, choices=[("0", "0"), ("1", "1")])
    weight = models.IntegerField()
    height = models.IntegerField()
    diabetes = models.CharField(max_length=2, choices=[("0", "0"), ("1", "1")])
    systolic = models.FloatField()
    diastolic = models.FloatField()
    cholesterol = models.IntegerField()
    hdl = models.FloatField()
    ldl = models.FloatField()
    triglycerides = models.IntegerField()
    smoking = models.CharField(max_length=2, choices=[("0", "0"), ("1", "1")])
    background = models.CharField(max_length=2, choices=[("0", "0"), ("1", "1")])
    estimation = models.FloatField()
    severity = models.CharField(max_length=10, default="Bajo")


class ResultsMedicPatient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.ForeignKey(Results, on_delete=models.CASCADE)
