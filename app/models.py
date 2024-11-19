import os
import uuid

from django.db import models


# generating random numbers for profile picture
def generate_unique_name(instance, filename):
    # kenya.png
    name = str(uuid.uuid4())  #
    full_file_name = f'{name}-{filename}'
    return os.path.join("profile_pictures", full_file_name)


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    weight = models.IntegerField(default=0)

    # profile picture
    profile_pic = models.ImageField(upload_to=generate_unique_name, null=True)
    # important to keep track of time for creation and update
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} "

    class Meta:
        db_table = 'customers'


class Deposit(models.Model):
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="deposits")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.first_name} has deposited Ksh {self.amount}"

    class Meta:
        db_table = 'deposits'

# run the migration
# python manage.py makemigrations
# python manage.py migrate

# to change portal python manage.py runserver 8001
