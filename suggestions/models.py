from django.db import models


# Create your models here.
class Suggestion(models.Model):
    name = models.CharField(max_length=100, null=False, )
    mobile_number = models.CharField(max_length=10, null=True)
    feedback = models.CharField(max_length=10000, null=False)
