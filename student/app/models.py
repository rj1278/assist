from django.db import models

# Create your models here.


class Department(models.Model):
    dept_name=models.CharField(max_length=50)
    dept_head=models.CharField(max_length=50)

class Student(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    department=models.ForeignKey(Department,related_name='dept',on_delete=models.PROTECT)

