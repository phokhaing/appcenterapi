#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : PHO KHAING                                     |
#  | EMAIL: khaing.pho1991@gmail.com                       |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 13.3.2023.                                   |
#  +-------------------------------------------------------+

from rest_framework import status
from rest_framework.response import Response


def ResponseSuccess(data: dict, message=None, status=status.HTTP_201_CREATED):
   return Response(
      {
         "success": True,
         "status" : status,
         "message": message,
         "data"   : data,
      }
   )


def ResponseFail(
        status=status.HTTP_404_NOT_FOUND,
        message="Fail, something went wrong!",
):
   return Response(
      {
         "success": False,
         "status" : status,
         "message": message,
         "data"   : None,
      }
   )
