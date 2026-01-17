from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
import pandas as pd
from common.permissions import IsAdmin, IsModeratorOrAdmin
from contacts.models import Contacts, StatusChoices
from .serializers import (
    ContactListSerializer,
    CreateContactsSerializer,
    UpdateStatusSerializer,
    ContactExportSerializer,
)
from rest_framework.generics import ListAPIView
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Language parameter (Global)
language_param = openapi.Parameter(
    'Accept-Language',
    openapi.IN_HEADER,
    description="Select language (uz=O'zbekcha, ru=Русский, en=English)",
    type=openapi.TYPE_STRING,
    required=False,
    default='uz',
    enum=['uz', 'ru', 'en']
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
        'new_leds': [AllowAny],
        'later': [AllowAny],
        'failed': [IsAdmin],
        'success_lead': [IsModeratorOrAdmin],
        'counts': [IsAdmin],
    }
    # authentication_classes = []

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

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get all contacts",
        operation_description="Retrieve list of all contacts with pagination support",
        responses={
            200: openapi.Response(
                description="Success",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT)
                        )
                    }
                )
            )
        },
        tags=['Contacts']
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": str(_("All contacts list")),
            "data": serializer.data
        })

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get single contact",
        operation_description="Retrieve detailed information about a specific contact",
        responses={
            200: openapi.Response(description="Success", schema=ContactListSerializer),
            404: "Contact not found"
        },
        tags=['Contacts']
    )
    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response({
            "success": True,
            "status": 200,
            "message": str(_("Single contact information")),
            "data": serializer.data
        })

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Create new contact",
        operation_description="Create a new contact entry. This endpoint is public (no authentication required).",
        request_body=CreateContactsSerializer,
        responses={
            201: openapi.Response(
                description="Contact created successfully",
                schema=CreateContactsSerializer
            ),
            400: "Validation error"
        },
        tags=['Contacts']
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 201,
                "message": str(_("Contact created successfully")),
                "data": serializer.data
            }, status=201)

        return Response({
            "success": False,
            "status": 400,
            "errors": serializer.errors
        }, status=400)

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Update contact (full)",
        operation_description="Fully update an existing contact. All fields are required.",
        request_body=UpdateStatusSerializer,
        responses={
            200: openapi.Response(description="Contact updated", schema=UpdateStatusSerializer),
            400: "Validation error",
            404: "Contact not found"
        },
        tags=['Contacts']
    )
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 200,
                "message": str(_("Contact fully updated")),
                "data": serializer.data
            })

        return Response({
            "success": False,
            "status": 400,
            "errors": serializer.errors
        }, status=400)

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Update contact (partial)",
        operation_description="Partially update an existing contact. Only provided fields will be updated.",
        request_body=UpdateStatusSerializer,
        responses={
            200: openapi.Response(description="Contact updated", schema=UpdateStatusSerializer),
            400: "Validation error",
            404: "Contact not found"
        },
        tags=['Contacts']
    )
    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "status": 200,
                "message": str(_("Contact partially updated")),
                "data": serializer.data
            })

        return Response({
            "success": False,
            "status": 400,
            "errors": serializer.errors
        }, status=400)

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Delete contact",
        operation_description="Permanently delete a contact from the system",
        responses={
            204: "Contact deleted successfully",
            404: "Contact not found"
        },
        tags=['Contacts']
    )
    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()

        return Response({
            "success": True,
            "status": 204,
            "message": str(_("Contact deleted"))
        }, status=204)

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get new leads",
        operation_description="Retrieve all contacts with 'New Lead' status",
        responses={200: ContactListSerializer(many=True)},
        tags=['Lead Management']
    )
    @action(detail=False, methods=['get'])
    def new_leds(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": str(_("New leads")),
            "data": serializer.data
        })

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get call back later leads",
        operation_description="Retrieve all contacts scheduled for callback later",
        responses={200: ContactListSerializer(many=True)},
        tags=['Lead Management']
    )
    @action(detail=False, methods=['get'])
    def later(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": str(_("Call back later leads")),
            "data": serializer.data
        })

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get failed leads",
        operation_description="Retrieve all contacts who don't need services",
        responses={200: ContactListSerializer(many=True)},
        tags=['Lead Management']
    )
    @action(detail=False, methods=['get'])
    def failed(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": str(_("Service not needed leads")),
            "data": serializer.data
        })

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get successful clients",
        operation_description="Retrieve all contacts who are using our services",
        responses={200: ContactListSerializer(many=True)},
        tags=['Lead Management']
    )
    @action(detail=False, methods=['get'])
    def success_lead(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "status": 200,
            "message": str(_("Clients working with us")),
            "data": serializer.data
        })

    @swagger_auto_schema(
        manual_parameters=[language_param],
        operation_summary="Get lead statistics",
        operation_description="Get count of leads by status (new, later, failed, success)",
        responses={
            200: openapi.Response(
                description="Lead counts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'new': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'later': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'failed': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'success': openapi.Schema(type=openapi.TYPE_INTEGER),
                            }
                        )
                    }
                )
            )
        },
        tags=['Statistics']
    )
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


class ExportAPIView(ListAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactExportSerializer
    permission_classes = [IsModeratorOrAdmin]

    @swagger_auto_schema(
        manual_parameters=[
            language_param,
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                description="Filter contacts by status before exporting",
                type=openapi.TYPE_STRING,
                required=False,
                enum=[choice.value for choice in StatusChoices]
            )
        ],
        operation_summary="Export contacts to Excel",
        operation_description="Export all contacts or filtered contacts to Excel file. "
                            "You can optionally filter by status and select language for column headers.",
        responses={
            200: openapi.Response(
                description="Excel file downloaded successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_FILE
                )
            )
        },
        tags=['Export']
    )
    def get(self, request, *args, **kwargs):
        # Status filter
        status_param = request.query_params.get("status")
        queryset = self.get_queryset()
        if status_param:
            queryset = queryset.filter(status_led=status_param)

        # Get data
        fields = self.serializer_class.Meta.fields
        contacts = queryset.values(*fields)
        df = pd.DataFrame(contacts)

        # Format created_at
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
            df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        filename = f"contacts__{timestamp}.xlsx"

        # Create Excel response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'

        df.to_excel(response, index=False)
        return response