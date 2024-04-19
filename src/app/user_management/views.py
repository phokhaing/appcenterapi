from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializer import UserDetailsSerializer


class UserManagement(viewsets.ModelViewSet):
   # authentication_classes = [TokenAuthentication]
   # permission_classes = [DjangoObjectPermissions]
   queryset = User.objects.all()
   serializer_class = UserDetailsSerializer


class CustomAuthToken(ObtainAuthToken):
   def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(data=request.data,
                                          context={'request': request})
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)
      return Response({
         'token': token.key,
         'user_id': user.pk,
         'email': user.email
      })

# method generated token data 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)

      # Add custom claims
      token['data'] = {
         "user_id": user.id, 
         "username": user.username, 
         "fullname": user.fullname, 
         "first_name": user.first_name,
         "last_name": user.last_name,
         "first_name_kh": user.first_name_kh,
         "last_name_kh": user.last_name_kh,
         "email": user.email,
         "gender": user.gender,
         "address": user.address,
         "phone_number": user.phone_number
      }
      return token

class MyTokenObtainPairView(TokenObtainPairView):
   serializer_class = MyTokenObtainPairSerializer


# class UserLogout(APIView):
#    authentication_classes = [TokenAuthentication]
#    # permission_classes = [IsAuthenticated]
#
#    def get(self, request):
#       request.user.auth_token.delete()
#       return Response({
#          'status': status.HTTP_200_OK,
#          'message': 'User logged out successfully',
#       })
