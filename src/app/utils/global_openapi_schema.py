#  +--------------------------------------------------------------+
#  | NAME : PHO KHAING                                            |
#  | EMAIL: khaing.pho@ftb.com.kh                                 |
#  | DUTY : FTB BANK (HEAD OFFICE)                                |
#  | ROLE : Full-Stack Software Developer                         |
#  +--------------------------------------------------------------|
#  | Released 20.08.2023.                                         |
#  | Description:  methods for data pagination by search, filter. |
#  +--------------------------------------------------------------+

from drf_yasg import openapi
from rest_framework import status
from django.db import models


def field_to_type(field):
    # Map Django field types to OpenAPI types
    if isinstance(field, models.CharField):
        return openapi.TYPE_STRING
    elif isinstance(field, models.IntegerField):
        return openapi.TYPE_INTEGER
    elif isinstance(field, models.BooleanField):
        return openapi.TYPE_BOOLEAN
    # Add more field type mappings as needed
    return openapi.TYPE_STRING  # Default to string if the type is not recognized


def global_response_openapi_shema(serializer):
    return {
        status.HTTP_201_CREATED: serializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    }


def global_request_openapi_schema(serializer):
    model_fields = serializer.Meta.model._meta.fields
    properties = {}

    for field in model_fields:
        field_type = field_to_type(field)
        properties[field.name] = openapi.Schema(
            type=field_type,
            description=field.verbose_name,
        )

    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties,
        required=[field.name for field in model_fields if not field.blank],
    )
