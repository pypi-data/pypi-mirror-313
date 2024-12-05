import json
from django.http import JsonResponse, HttpResponse

from sentry_sdk import capture_exception


class CaptureExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if exception:
            capture_exception(exception)
            return JsonResponse(
                {"success": False, "detail": str(exception)}, status=500
            )


class ValidationErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: HttpResponse = self.get_response(request)

        content_type = response.headers.get("Content-Type")
        if (
                content_type
                and content_type == "application/json"
                and response.status_code == 400
        ):
            data = json.loads(response.content)
            if (
                    isinstance(data, dict)
            ):
                data.pop("success", None)
                errors = data
                if errors.get('detail'):
                    errors = errors.get('detail')
                elif errors.get('errors'):
                    errors = errors.get('errors')
                elif errors.get('error'):
                    errors = errors.get('error')
                data = {"success": False, "errors": errors}

            response.content = json.dumps(data)

        return response
