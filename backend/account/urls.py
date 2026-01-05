from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomLoginView, CustomRefreshView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')  # '' emas, 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshView.as_view(), name='token_refresh'),
] + router.urls
