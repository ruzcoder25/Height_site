from django.urls import path
from rest_framework.routers import DefaultRouter
from account.views import UserViewSet, CustomLoginView, CustomRefreshView


router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshView.as_view(), name='token_refresh'),
] + router.urls
