from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.db import models


class GroupDetail(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    group_name = models.CharField(max_length=50)
    number_of_people = models.PositiveIntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name


class PersonDetail(models.Model):
    group_id = models.ForeignKey(GroupDetail, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100, default='NA')
    units_per_person = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.group_id) + ' ---> ' + str(self.person_name)


class ShareDetail(models.Model):
    group_id = models.ForeignKey(GroupDetail, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    share_per_person = models.CharField(validators=[validate_comma_separated_integer_list], max_length=10000, blank=True,
                                        null=False)
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.group_id) + ' ---> ' + str(self.description) + ' ---> ' + str(
            self.total_price) + ' ---> ' + str(self.last_updated)


class ResultDetail(models.Model):
    group_id = models.ForeignKey(GroupDetail, on_delete=models.CASCADE)
    owe_by = models.CharField(max_length=100)
    owe_to = models.CharField(max_length=100)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.group_id) + ' ---> ' + str(self.owe_by) + ' ---> ' + str(
            self.owe_to) + ' ---> ' + str(self.amount)