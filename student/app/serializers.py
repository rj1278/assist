
from itertools import count
from pyexpat import model
from urllib import request
from attr import field, fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student,Department
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
# from django.contrib.auth import authenticate

class StudentSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Student
        fields=['id','first_name','last_name']

class UpdateStudentSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    class Meta:
        model=Student
        fields=['id','first_name','last_name','department']


class DepartmentSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'
    

class NestedStudentSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    students=StudentSerializer(many=True,source='dept')
    
    class Meta:
        model=Department
        fields=['id','dept_name','dept_head','students']
class UpdateNestedStudentSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    students=UpdateStudentSerializer(many=True)
    class Meta:
        model=Department
        fields=['id','dept_name','dept_head','students']


class CRUDStudentSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    full_name=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Student
        fields=['id','first_name','last_name','department','full_name']

    def get_full_name(self,obj):
        return f'{obj.first_name} {obj.last_name}'



class FindStudentInDptSerializer(serializers.ModelSerializer):

    department=serializers.CharField(source='dept_name')
    student_count=serializers.SerializerMethodField()
    class Meta:
        model=Department
        fields=['department','student_count']
    def get_student_count(self,obj):
        model=Student.objects.filter(department=obj.id).count()
        return model
    

