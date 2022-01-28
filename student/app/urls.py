
from django.db import router
from django.urls import path,include
from rest_framework.routers import DefaultRouter,SimpleRouter
from . import viewsets

router=DefaultRouter()
router.register('create',viewsets.CreateStudentViewset)
router.register('crud',viewsets.CRUDViewset)
router.register('list',viewsets.ListDeptViewset)
router.register('list',viewsets.UpdateNestedViewset)

urlpatterns=[
    path('',include(router.urls))

]

