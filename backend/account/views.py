from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from common.permissions import IsAdmin
from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CreateAndUpdateUserSerializer,
    UserListSerializer
)

# ============================
# LOGIN VIEW (faqat POST)
# ============================
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]  # Har kim kirishi mumkin


# ============================
# REFRESH VIEW (faqat POST)
# ============================
class CustomRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = [AllowAny]  # Har kim kirishi mumkin

# ============================
# USER VIEWSET
# ============================
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
        if self.action in ['create', 'destroy', 'update', 'partial_update', 'list']:
            return [IsAuthenticated(), IsAdmin()]
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        return [AllowAny()]

    # Optional: override response messages
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "success": True,
            "status": 201,
            "message": "Foydalanuvchi yaratildi",
            "data": serializer.data
        }, status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "success": True,
            "status": 200,
            "message": "Foydalanuvchi yangilandi",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "status": 204,
            "message": "Foydalanuvchi o‘chirildi"
        }, status=204)
