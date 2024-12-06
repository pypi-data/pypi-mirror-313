from rest_framework.authentication import BasicAuthentication

class BasicLikeAuthentication(BasicAuthentication):
    def authenticate_header(self, request):
        return f'BasicLike realm="{self.www_authenticate_realm}"'