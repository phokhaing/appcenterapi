from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import create_leave_balance, list_leave_balances, \
    update_leave_balance, delete_leave_balance, fetch_one_leave_balance
from rest_framework import viewsets

router = DefaultRouter()
urlpatterns = [
    path('create/', create_leave_balance, name='create-leave-balance'),
    path('list/', list_leave_balances, name='list-leave-balance'),
    path('fetch-one/<uuid:pk>/', fetch_one_leave_balance, name='fetch-one-leave-balance'),
    path('update/<uuid:pk>/', update_leave_balance, name='update-leave-balance'),
    path('delete/<uuid:pk>/', delete_leave_balance, name='delete-leave-balance'),

] + router.urls
