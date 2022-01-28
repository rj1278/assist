from rest_framework.schemas.openapi import AutoSchema
from .models import Student,Department
from rest_framework import viewsets,generics
from .serializers import UpdateNestedStudentSerializer,NestedStudentSerializer,FindStudentInDptSerializer,CRUDStudentSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.authentication import BaseAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action


class CreateStudentViewset(viewsets.GenericViewSet):
    schema=AutoSchema(tags=['Question 3 : Nested Response Of Student Create List Retrieve Update'])
    serializer_class=NestedStudentSerializer
    queryset=Department.objects.all()
    def create(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            dept_student=data.pop('students')
            department=Department.objects.create(**data)
            for student in dept_student:
                Student.objects.create(department=department,**student)
            return Response({'status':status.HTTP_201_CREATED,'message':'Student Object Created Successfully'})
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
    def list(self,request):
        serializer=self.get_serializer(self.get_queryset(),many=True)
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class UpdateNestedViewset(viewsets.GenericViewSet):
    schema=AutoSchema(tags=['Question 3 : Nested Response Of Student Create List Retrieve Update'])
    serializer_class=UpdateNestedStudentSerializer
    queryset=Department.objects.all()
    @action(methods=['put'],detail=False)
    def update_std(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            dept_student=data.pop('students')
            department=Department.objects.filter(pk=data['id']).update(dept_name=data['dept_name'],
            dept_head=data['dept_head'])
            for student in dept_student:
                Student.objects.filter(pk=student['id']).update(department=data['id'],
                first_name=student['first_name'],last_name=student['last_name'])
            return Response({'status':status.HTTP_200_OK,'message':'Student Object Updated Successfully'})
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})



class CRUDViewset(viewsets.ModelViewSet):
    schema=AutoSchema(tags=['Question 1  and Question 2:Student CRUD Controller'])
    serializer_class=CRUDStudentSerializer
    queryset=Student.objects.all()

class ListDeptViewset(viewsets.GenericViewSet):
    schema=AutoSchema(tags=['Question 4 : Django ORM to list students'])
    serializer_class=FindStudentInDptSerializer
    queryset=Department.objects.all()
    def list(self,request):
        serializer=self.get_serializer(self.get_queryset(),many=True)
        print(serializer.data)
        data=[]
        for i in serializer.data:
            if not any(d['department'] == i['department'] for d in data):
                data.append(i)
            else:
                for j in data:
                    if j['department'] == i['department']:
                        j['student_count'] = j['student_count'] + i['student_count']
        return Response(data)

# class ListFullNameViewset(viewsets.GenericViewSet):
#     schema=AutoSchema(tags=['Question 2 : End points with FullName '])
#     serializer_class=CRUDStudentSerializer
#     queryset=Student.objects.all()
#     def list(self,request):
#         serializer=self.get_serializer(self.get_queryset(),many=True)
#         return Response(serializer.data)



