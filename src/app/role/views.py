from rest_framework import viewsets
from .serializer import RoleSerializer
from .models import Role


class RoleController(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
