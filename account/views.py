from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from common.permissions import IsAdmin
from .models import User
from account.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CreateAndUpdateUserSerializer,
    UserListSerializer
)


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateAndUpdateUserSerializer
        elif self.action in ['list', 'retrieve']:
            return UserListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['list']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['retrieve']:
            return [IsAuthenticated()]
        return [AllowAny()]
