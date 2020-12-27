"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
# Permissions
from rest_framework.permissions import (	
	IsAuthenticated,
    AllowAny
)
from .permissions import IsAccountOwner

# Serializers
from api.crm.serializers import (UserModelSerializer, 
                                UserCreateSerializer, 
                                UserUpdateModelSerializer, 
                                UserLoginSerializer, 
                                RetrieveUserModelSerializer, 
                                UserListModelSerializer,
                                ChangePasswordSerializer)

# Models
from api.crm.models import User

#Filters
from django_filters import rest_framework as filters

from rest_framework.permissions import IsAuthenticated



class UserViewSet(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin):
    
    queryset = User.objects.all()    
    lookup_field = 'username'
    filter_backends = (filters.DjangoFilterBackend,)

    def get_permissions(self):
        if self.action in ['login']:
            permissions = [AllowAny]
        if self.action in ['partial_update']:
            permissions = [IsAccountOwner]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    def get_serializer_class(self):        
        if self.action == 'partial_update':
            return UserUpdateModelSerializer
        if self.action == 'retrieve':
            return RetrieveUserModelSerializer
        if self.action == 'list':
            return UserListModelSerializer
        else:
            return UserModelSerializer

    class UserFilter(filters.FilterSet):
        class Meta:
            model = User
            fields = {
                'first_name': ['contains', 'exact'],
                'last_name': ['contains', 'exact'],
                'email': ['contains', 'exact'],
                'created': [
                    'contains', 
                    'gte', 
                    'lte', 
                    'year', 
                    'month', 
                    'day', 
                    'year__range', 
                    'month__range', 
                    'day__range', 
                    'date__range'
                ],
            }

    filterset_class = UserFilter

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)           
            
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserLoginSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
        
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class=ChangePasswordSerializer
    model=User
    queryset=User.objects.all()
    permission_classes=[IsAccountOwner]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)        
        if serializer.is_valid():
            self.object.set_password(serializer.data.get('password_confirmation'))
            self.object.save()
            
            get_user = User.objects.filter(email=request.user).first().id            
            Token.objects.filter(user=get_user).delete()  

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'La contraseña ha sido actualizada y su token de seguridad fue eliminado debe volver a iniciar sesion',
                'data': []
            }
            
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)