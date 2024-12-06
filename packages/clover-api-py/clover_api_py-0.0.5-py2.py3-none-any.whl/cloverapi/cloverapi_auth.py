from requests.auth import AuthBase

class CloverApiAuth(AuthBase):
    """
    Custom AuthBase class for Clover API Bearer Token authentication.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, request):
        """
        Update the request with Authorization headers for Bearer token.
        """
        request.headers.update({
            'Content-Type': 'Application/JSON',
            'Authorization': f'Bearer {self.api_key}'
        })
        return request