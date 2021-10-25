from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.micro.dorm import Dorm
from apps.micro.serializers import DormSerializer
from utils.auth import Authentication
from utils.custom_response.base_constant import *
from utils.custom_response.base_response import BaseResponse


class DormViewSet(mixins.CreateModelMixin,
                  GenericViewSet):
    serializer_class = DormSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        dorm = Dorm()
        try:
            dushu = dorm.get_ele(request.data)
        except Exception as e:
            return BaseResponse(code=CODE_METHOD_ERROR, message=str(e))
        return BaseResponse(data=dushu)
