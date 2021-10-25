from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


def verify_token(request):
    """
    验证token，防止接口被滥用
    :return:
    """
    # do something
    return True


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        res = verify_token(request)
        if not res:
            raise exceptions.AuthenticationFailed('认证失败')
        token = request.META.get('HTTP_TOKEN')
        return token, token
