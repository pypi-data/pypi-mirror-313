import requests


class BaseRequest:
    base_url = None

    def __init__(self, request):
        header = request.META.get("HTTP_AUTHORIZATION", None)
        parts = header.split()
        if len(parts) == 0:
            raise Exception("Empty AUTHORIZATION header sent")
        if len(parts) != 2:
            raise Exception(
                'Authorization header must contain two space-delimited values'
            )
        self.token = parts[1]

    def send_request(self, method, path, data=None):
        headers = {'Accept': 'application/json', 'Authorization': f'Bearer {str(self.token)}',
                   'Content-Type': 'application/json'}
        try:

            res = requests.request(method=method, url=f"{self.base_url}/{path}", json=data, headers=headers, verify=False)
        except Exception as err:
            raise Exception(f"Error occurred: {err}") from err
        if 200 <= res.status_code < 300:
            return res.json()
        else:
            raise Exception(f"Error occurred: {res.text}")
