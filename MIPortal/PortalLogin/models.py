from django.db import models
import uuid

# Create your models here.


class Lead(models.Model):
    type = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)


class Turnover(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    value = models.CharField(max_length=50, null=True, blank=True)
    number = models.IntegerField(null=True)


class State(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
