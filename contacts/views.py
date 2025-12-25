from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
import pandas as pd
from common.permissions import IsAdmin, IsModeratorOrAdmin
from contacts.models import Contacts, StatusChoices
from .serializers import (
    ContactListSerializer,
    CreateContactsSerializer,
    UpdateStatusSerializer, ContactExportSerializer,
)
from rest_framework.generics import ListAPIView
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



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
        'counts': [IsAdmin],

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
        elif self.action == "success_lead":
            qs = qs.filter(status_led=StatusChoices.SUCCESS)

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

    @action(detail=False, methods=['get'])
    def success_lead(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": "Biz bilan hamkorlik qilayotgan mijozlar ro'yhati",
            "data": serializer.data
        })

    @action(detail=False, methods=["get"])
    def counts(self, request):
        return Response({
            "success": True,
            "status": 200,
            "data": {
                "new": Contacts.objects.filter(status_led=StatusChoices.NEW_LED).count(),
                "later": Contacts.objects.filter(status_led=StatusChoices.LATER).count(),
                "failed": Contacts.objects.filter(status_led=StatusChoices.FAILED).count(),
                "success": Contacts.objects.filter(status_led=StatusChoices.SUCCESS).count(),
            }
        })

#
# class ImportAPIView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#
#     def post(self, request):
#         try:
#             file = request.FILES.get("file")
#             if not file:
#                 return Response({"error": "Fayl topilmadi"}, status=400)
#
#             df = pd.read_excel(file)
#
#             contacts = []
#
#             for _, row in df.iterrows():
#                 contacts.append(Contacts(
#                     full_name=row.get('full_name'),
#                     phone_number=row.get('phone_number'),
#                     business_name=row.get('business_name'),
#                     user_comment=row.get('user_comment'),
#                     service_type=row.get('service_type'),
#                     status_led=row.get('status_led'),
#                     call_time=row.get('call_time'),
#                     month=row.get('month'),
#                     day=row.get('day'),
#                     year=row.get('year')
#                 ))
#
#             Contacts.objects.bulk_create(contacts)
#
#             return Response({
#                 "success": True,
#                 "message": f"{len(contacts)} ta kontakt yuklandi"
#             }, status=201)
#
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)


class ExportAPIView(ListAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactExportSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                description="Filter by status",
                type=openapi.TYPE_STRING,
                enum=[choice.value for choice in StatusChoices]
            )
        ],
        operation_description="Export Contacts to Excel. Optionally filter by status",
        responses={200: "Excel file"}
    )
    def get(self, request, *args, **kwargs):
        # 1️⃣ Status filter
        status_param = request.query_params.get("status")
        queryset = self.get_queryset()
        if status_param:
            queryset = queryset.filter(status_led=status_param)

        # 2️⃣ Kerakli maydonlar
        fields = self.serializer_class.Meta.fields
        contacts = queryset.values(*fields)
        df = pd.DataFrame(contacts)


        # 4️⃣ created_at formatlash
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
            df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")


        timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        filename = f"contacts__{timestamp}.xlsx"

        # 6️⃣ Excel response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'

        df.to_excel(response, index=False)
        return response