import os
import json
import uuid
import traceback
from datetime import datetime
from threading import Lock

from django.conf import settings
from django.http import JsonResponse, Http404
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
    Throttled
)
from rest_framework.response import Response


class GlobalExceptionLoggingMiddleware:
    """
    Universal Exception Logging Middleware
    - Django & DRF compatible
    - Thread-safe
    - Logs unhandled errors to JSON file
    - Returns JSON response for all exceptions
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.file_lock = Lock()

        # Log file path (default: <BASE_DIR>/logs/unhandled_errors.json)
        default_log_dir = os.path.join(getattr(settings, "BASE_DIR", "."), "logs")
        os.makedirs(default_log_dir, exist_ok=True)
        self.log_file = getattr(
            settings, 
            "UNHANDLED_ERROR_LOG_FILE", 
            os.path.join(default_log_dir, "unhandled_errors.json")
        )

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as exc:
            return self.process_exception(request, exc)
        return response

    def process_exception(self, request, exception):
        status_code = self.get_status_code_from_exception(exception)

        # Faqat status 401, 400, 404, 403, 429 bo‘lmaganlar log qilinadi
        if status_code not in [400, 401, 403, 404, 429]:
            self.log_unhandled_error(exception, request)

        payload = {
            "success": False,
            "message": "Serverda kutilmagan xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring.",
            "error_detail": str(exception)
        }

        # DEBUG mode’da traceback qo‘shiladi
        if getattr(settings, "DEBUG", False):
            payload["traceback"] = traceback.format_exc()

        # DRF bilan mos kelish uchun Response ishlatish
        try:
            from rest_framework.response import Response
            return Response(payload, status=status_code)
        except ImportError:
            return JsonResponse(payload, status=status_code, json_dumps_params={"ensure_ascii": False})

    def get_status_code_from_exception(self, exception):
        if isinstance(exception, Http404):
            return 404
        elif isinstance(exception, PermissionDenied):
            return 403
        elif isinstance(exception, (AuthenticationFailed, NotAuthenticated)):
            return 401
        elif isinstance(exception, ValidationError):
            return 400
        elif isinstance(exception, Throttled):
            return 429
        elif hasattr(exception, "status_code") and isinstance(exception.status_code, int):
            return exception.status_code
        return 500

    def log_unhandled_error(self, exception, request):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_data = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "method": request.method,
            "path": request.get_full_path(),
            "user_id": getattr(request.user, 'id', None),
            "error": repr(exception),
            "traceback": traceback.format_exc() if getattr(settings, "DEBUG", False) else None
        }

        # Faylga thread-safe yozish
        with self.file_lock:
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []

            logs.append(error_data)

            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=4)
