from django.db import models
from security.models import CustomUser

class User(models.Model):
    firstname = models.TextField(null=False)
    lastname = models.TextField(null=False)
    address = models.TextField(null=False)
    email= models.TextField(null=False)
    national_id = models.TextField(null=False)
    national_id_type = models.TextField(null=False)
    country = models.TextField(null=False)
    security_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='security')
