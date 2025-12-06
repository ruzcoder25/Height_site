from rest_framework.routers import DefaultRouter
from .views import ContactViewSet
from . import views
from django.urls import path

router = DefaultRouter()
router.register('contacts', ContactViewSet)


urlpatterns = [
    # path('import-exel/',views.ImportAPIView.as_view()),
    path('export-exel/',views.ExportAPIView.as_view()),


]+router.urls