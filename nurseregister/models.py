from django.db import models
from simple_history.models import HistoricalRecords

class NurseRegistration(models.Model):
    name = models.CharField(max_length=2048)

    history = HistoricalRecords()

class MyNewModel(models.Model):
    name = models.CharField(max_length=2048)

    history = HistoricalRecords()
