from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.permissions import IsAdmin, IsModeratorOrAdmin
from contacts.models import Contacts, StatusChoices
from .serializers import (
    ContactListSerializer,
    CreateContactsSerializer,
    UpdateStatusSerializer
)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactListSerializer
    permission_classes_by_action = {
        'list': [IsModeratorOrAdmin],
        'retrieve': [IsModeratorOrAdmin],
        'create': [AllowAny],
        'update': [IsAdmin],
        'partial_update': [AllowAny],
        'destroy': [IsAdmin],

        # custom action
        'new_leds': [AllowAny],
        'later': [AllowAny],
        'failed': [IsAdmin],
    }

    def get_permissions(self):
        try:
            return [perm() for perm in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [AllowAny()]

    def get_queryset(self):
        qs = Contacts.objects.all()

        if self.action == "new_leds":
            qs = qs.filter(status_led=StatusChoices.NEW_LED)
        elif self.action == "later":
            qs = qs.filter(status_led=StatusChoices.LATER)
        elif self.action == "failed":
            qs = qs.filter(status_led=StatusChoices.FAILED)

        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return CreateContactsSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateStatusSerializer
        return ContactListSerializer


    def list(self, request):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Barcha kontaktlar ro'yhati",
            "data": serializer.data
        })

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response({
            "success": True,
            "status": 200,
            "message": "Bitta kontakt ma'lumotlari",
            "data": serializer.data
        })

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 201,
                "message": "Kontakt muvaffaqiyatli yaratildi",
                "data": serializer.data
            }, status=201)

        return Response({
            "success": False,
            "status": 400,
            "errors": serializer.errors
        }, status=400)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 200,
                "message": "Kontakt to‘liq yangilandi",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 200,
                "message": "Kontakt qisman yangilandi (status yoki izoh)",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()

        return Response({
            "success": True,
            "status": 204,
            "message": "Kontakt o‘chirildi"
        }, status=204)


    @action(detail=False, methods=['get'])
    def new_leds(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Yangi leadlar",
            "data": serializer.data
        })

    @action(detail=False, methods=['get'])
    def later(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Keyinroq qo'ng'iroq qilinadigan leadlar",
            "data": serializer.data
        })

    @action(detail=False, methods=['get'])
    def failed(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Hizmatlar kerak bo‘lmagan leadlar",
            "data": serializer.data
        })
