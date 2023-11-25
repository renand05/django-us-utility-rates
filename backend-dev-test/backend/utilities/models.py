from django.db import models

class User(models.Model):
    firstname = models.TextField(null=False)
    lastname = models.TextField(null=False)
    address = models.TextField(null=False)
    email= models.TextField(null=False)
    national_id = models.TextField(null=False)
    national_id_type = models.TextField(null=False)
    country = models.TextField(null=False)
