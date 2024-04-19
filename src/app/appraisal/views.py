#  +-------------------------------------------------------+
#  | NAME  : PHO KHAING                                    |
#  | EMAIL : khaing.pho1991@ftbbank                        |
#  | DUTY  : FTB BANK (HEAD OFFICE)                        |
#  | ROLE  : Full-Stack Software Developer                 |
#  +-------------------------------------------------------+
#  | Copyright (c) 2022.                                   |
#  | Released 30.7.2022.                                   |
#  +-------------------------------------------------------+

from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import (
   api_view,
   permission_classes,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Appraisal
from .serializer import AppraisalSerializer
from ..utils.ApiResponse import ResponseSuccess, ResponseFail


# -------------------------------------
#  API_VIEW
# -------------------------------------
@api_view(["GET"])
def ApiOverview(request):
   return Response(
      [
         "/api/appraisal",
         {
            "Lists" : "/all",
            "View"  : "/view/pk",
            "Add"   : "/create/",
            "Update": "/update/pk",
            "Delete": "/update/pk",
         },
      ]
   )


# -------------------------------------
#  Method for list all data
# -------------------------------------
@api_view(["GET"])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])  # Token Authentication
def list_appraisal(request):
   paginator = PageNumberPagination()
   appraisal = Appraisal.objects.all()
   context = paginator.paginate_queryset(appraisal, request)
   serializer = AppraisalSerializer(context, many=True)
   
   return paginator.get_paginated_response(
      {
         "success": True,
         "status" : status.HTTP_200_OK,
         "message": "List all appraisal records",
         "data"   : serializer.data,
      }
   )


# -------------------------------------
#  Method for create new data
# -------------------------------------
@api_view(["POST"])
def create_appraisal(request):
   serializer = AppraisalSerializer(data=request.data)
   if Appraisal.objects.filter(**request.data).exists():
      raise serializers.ValidationError("This data already exists!")
   
   if serializer.is_valid():
      serializer.save()
      return ResponseSuccess(
         data=serializer.data, message="Appraisal data saved successfully!"
      )
   
   return ResponseFail(message="Fail, something went wrong!")


# -------------------------------------
#  Method for update exists data by id
# -------------------------------------
@api_view(["PUT"])
def update_appraisal(request, id):
   appraisal = Appraisal.objects.get(id=id)
   serializer = AppraisalSerializer(instance=appraisal, data=request.data)
   
   context = {
      "success": False,
      "status" : status.HTTP_400_BAD_REQUEST,
      "message": "Fail, something went wrong!!.",
      "data"   : None,
   }
   if serializer.is_valid():
      serializer.save()
      context["success"] = True
   
   return Response(context)


# -------------------------------------
#  Method for delete exists data by id
# -------------------------------------
@api_view(["DELETE"])
def delete_appraisal(request, pk):
   serializer = get_object_or_404(Appraisal, pk=pk)
   serializer.delete()
   return Response(
      {
         "success": True,
         "status" : status.HTTP_202_ACCEPTED,
         "message": "Appraisal deleted successfully.",
      }
   )


# -------------------------------------
#  Method for view data by id
# -------------------------------------
@api_view(["GET"])
def view_appraisal(request, id=None):
   appraisal = get_object_or_404(Appraisal, id=id)
   serializer = AppraisalSerializer(appraisal)
   return Response(
      {
         "success": True,
         "status" : status.HTTP_200_OK,
         "message": "List all appraisal records",
         "data"   : serializer.data,
      }
   )
