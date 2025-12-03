from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet)


urlpatterns = [
    # path('add-contact/',views.ContactsCreateAPIView.as_view()),
    # path('list-contact/',views.ListContactAPIView.as_view()),


]+router.urls