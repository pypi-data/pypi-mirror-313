from datetime import datetime
import os

from .base import BaseRequest


class AuthService(BaseRequest):
    base_url = None

    def __init__(self, request):
        super().__init__(request)
        base_url = f"{os.getenv('AUTH_SERVICE_BASE_URL', None)}/api/v1"
        self.base_url = f"{base_url}"

    def get_user_by_id(self, id):
        path = f'users/{id}'
        return self.send_request("GET", path)


def get_auth_token(request=None):

    if request is None:
        return {}
   
    request_time=datetime.now()
    request_time = request_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    if isinstance(request, dict):
        auth_token = request['headers']["Authorization"]
    else:
       auth_token = request.headers.get("Authorization")
    auth_token = auth_token.split()[1] if "Bearer" in auth_token else auth_token
    return {"Authorization": f"Bearer {auth_token}"}
