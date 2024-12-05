import json
import time

from django.conf import settings
from django.urls import Resolver404, resolve
from django.utils import timezone
from rest_framework.urls import app_name

from .encoder import MongoEncoder
from .tasks import send_logs_to_logger
from .contrib import get_headers, get_client_ip, mask_sensitive_data, decode_jwt_token


class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Initialize settings from Django settings or use defaults
        self.API_LOGGER_PATH_TYPE = getattr(settings, 'API_LOGGER_PATH_TYPE', 'ABSOLUTE')
        if self.API_LOGGER_PATH_TYPE not in ['ABSOLUTE', 'RAW_URI', 'FULL_PATH']:
            self.API_LOGGER_PATH_TYPE = 'ABSOLUTE'

        self.API_LOGGER_SKIP_URL_NAME = getattr(settings, 'API_LOGGER_SKIP_URL_NAME', [''])
        if not isinstance(self.API_LOGGER_SKIP_URL_NAME, (tuple, list)):
            self.API_LOGGER_SKIP_URL_NAME = ['']

        self.API_LOGGER_SKIP_NAMESPACE = getattr(settings, 'API_LOGGER_SKIP_NAMESPACE', [])
        if not isinstance(self.API_LOGGER_SKIP_NAMESPACE, (tuple, list)):
            self.API_LOGGER_SKIP_NAMESPACE = []

        self.API_LOGGER_CONTENT_TYPES = [
            "application/json",
            "application/vnd.api+json",
            "application/gzip",
            "application/octet-stream",
        ]

        self.API_LOGGER_EXCLUDE_HTTP_METHODS = ['GET']
        if hasattr(settings, 'API_LOGGER_EXCLUDE_HTTP_METHODS'):
            if type(settings.API_LOGGER_EXCLUDE_HTTP_METHODS) is tuple or type(
                    settings.API_LOGGER_EXCLUDE_HTTP_METHODS) is list:
                self.API_LOGGER_EXCLUDE_HTTP_METHODS = [
                    item.upper() for item in settings.API_LOGGER_EXCLUDE_HTTP_METHODS]

    def __call__(self, request):
        try:
            if hasattr(settings, 'MONGODB_LOGGER_URL'):
                method = request.method
                # Resolve URL name and namespace
                try:
                    resolver_match = resolve(request.path_info)
                    url_name = resolver_match.url_name
                    namespace = resolver_match.namespace
                except Resolver404:
                    resolver_match = None
                    url_name = None
                    namespace = None

                # Always skip logging for requests in 'admin' namespace
                if namespace == 'admin':
                    return self.get_response(request)

                # Skip logging based on configured URL names
                if url_name in self.API_LOGGER_SKIP_URL_NAME:
                    return self.get_response(request)

                # Skip logging based on configured namespaces
                if namespace in self.API_LOGGER_SKIP_NAMESPACE:
                    return self.get_response(request)

                if len(self.API_LOGGER_EXCLUDE_HTTP_METHODS) > 0 and method in self.API_LOGGER_EXCLUDE_HTTP_METHODS:
                    return self.get_response(request)

                # Measure request execution time
                start_time = time.time()

                # Fetch request headers and method
                headers = get_headers(request=request)
                method = request.method

                # Parse request body based on content type
                request_data = {}
                if request.content_type == "application/json":
                    try:
                        request_data = json.loads(request.body)
                    except json.JSONDecodeError:
                        request_data = request.body.decode('utf-8')
                elif request.content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
                    request_data = request.POST.dict()
                    if request.FILES:
                        request_data['files'] = {key: file.name for key, file in request.FILES.items()}

                view_action_name = None
                view_action_doc = None
                if resolver_match:
                    view_func = resolver_match.func
                    view_cls = getattr(view_func, 'cls', None)
                    request_method = request.method.lower()

                    if hasattr(view_func, 'actions'):
                        # Try to get the action method name from view_func.actions for the request method
                        view_action_name = view_func.actions.get(request_method)
                        if view_action_name and view_cls:
                            view_action_func = getattr(view_cls, view_action_name, None)
                            view_action_doc = getattr(view_action_func, '__doc__', None)
                    elif view_cls:
                        # If no specific action is defined, fall back to method or class doc
                        view_action_name = request_method if hasattr(view_cls, request_method) else view_cls.__name__
                        view_action_doc = getattr(getattr(view_cls, request_method, None), '__doc__',
                                                  None) or view_cls.__doc__

                email, user_id, fullname = decode_jwt_token(request)
                response = self.get_response(request)

                # Determine response body based on content type
                if response.get("content-type") in self.API_LOGGER_CONTENT_TYPES:
                    if response.get('content-type') == 'application/gzip':
                        response_body = '** GZIP Archive **'
                    elif response.get('content-type') == 'application/octet-stream':
                        response_body = '** Binary File **'
                    elif getattr(response, 'streaming', False):
                        response_body = '** Streaming **'
                    else:
                        if isinstance(response.content, bytes):
                            response_body = json.loads(response.content.decode())
                        else:
                            response_body = json.loads(response.content)

                    # Determine API path based on configuration
                    if self.API_LOGGER_PATH_TYPE == 'ABSOLUTE':
                        api = request.build_absolute_uri()
                    elif self.API_LOGGER_PATH_TYPE == 'FULL_PATH':
                        api = request.get_full_path()
                    elif self.API_LOGGER_PATH_TYPE == 'RAW_URI':
                        api = request.get_raw_uri()
                    else:
                        api = request.build_absolute_uri()

                    # Mask sensitive data in the logged data
                    data = dict(
                        app_name=settings.APP_NAME.lower(),
                        api=mask_sensitive_data(api, mask_api_parameters=True),
                        headers=mask_sensitive_data(headers),
                        body=mask_sensitive_data(request_data),
                        method=method,
                        client_ip_address=get_client_ip(request),
                        response=mask_sensitive_data(response_body),
                        status_code=response.status_code,
                        execution_time=time.time() - start_time,
                        added_on=str(timezone.now()),
                        email=email,
                        user_id=user_id,
                        fullname=fullname,
                        action_description=view_action_doc,
                        action_function_call=view_action_name,
                        environment=settings.ENVIRONMENT_INSTANCE,
                    )

                    # Convert certain fields to JSON for logging purposes
                    d = data.copy()
                    d['headers'] = json.dumps(d['headers'], indent=4, ensure_ascii=False) if d.get('headers') else {}
                    if request_data:
                        d['body'] = json.dumps(d['body'], indent=4, ensure_ascii=False) if d.get('body') else {}
                    d['response'] = json.dumps(d['response'], indent=4, ensure_ascii=False) if d.get('response') else {}
                    if method not in ['get', 'GET']:
                        # json_data = json.dumps(d, cls=MongoEncoder, indent=4)
                        send_logs_to_logger.delay(data)

            else:
                response = self.get_response(request)
            return response

        except Exception:
            return self.get_response(request)
