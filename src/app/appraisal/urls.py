#  +-------------------------------------------------------+
#  | Copyright (c) 2022.                                   |
#  +-------------------------------------------------------+
#  | NAME  : PHO KHAING                                    |
#  | EMAIL : khaing.pho1991@gmail.com                      |
#  | DUTY  : FTB BANK (HEAD OFFICE)                        |
#  | ROLE  : Full-Stack Software Developer                 |
#  +-------------------------------------------------------+
#  | Released 30.7.2022.                                   |
#  +-------------------------------------------------------+


from django.urls import path
from . import views

urlpatterns = [
   path('', views.ApiOverview, name='appraisal'),
   path('all', views.list_appraisal, name='list-appraisal'),
   path('view/<int:id>/', views.view_appraisal, name='view-appraisal'),
   path('create/', views.create_appraisal, name='create-appraisal'),
   path('update/<int:id>/', views.update_appraisal, name='update-appraisal'),
   path('delete/<int:pk>/', views.delete_appraisal, name='delete-appraisal')

]
