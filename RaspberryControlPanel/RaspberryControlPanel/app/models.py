"""
Definition of models.
"""

from django.db import models

# Create your models here.
class BaseProperty(models.Model):

    cpu_data = models.CharField(max_length=200)
    ram_data = models.CharField(max_length=200)
    hd_data = models.CharField(max_length=200)
    netio_data = models.CharField(max_length=200)
    netint_data = models.CharField(max_length=200)
    

    pass