from django.db import models

# Create your models here.


class Student(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_name
