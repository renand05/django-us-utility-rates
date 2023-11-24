from django.db import models

class User(models.Model):
    firstname = models.TextField(default='')
    lastname = models.TextField(default='')
    address = models.TextField(default='')