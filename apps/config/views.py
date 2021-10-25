from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import GenericViewSet

from apps.config.models import Carousel, Tips
from apps.config.serializers import CarouselSerializer, TipsSerializer
from utils.auth import Authentication
from utils.custom_page_set import PageSet
from utils.custom_response.base_response import BaseResponse


class CarouselViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    """
    轮播图api接口
    """
    serializer_class = CarouselSerializer
    authentication_classes = [Authentication, ]
    queryset = Carousel.objects.all()
    pagination_class = PageSet

    def get_queryset(self):
        qs = super().get_queryset()  # 调用父类方法
        return qs.filter(status=1).order_by('index')

    def list(self, request, *args, **kwargs):
        response = super(CarouselViewSet, self).list(request, *args, **kwargs)
        return BaseResponse(data=response.data)


class TipsViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    """
    贴士api接口
    """
    serializer_class = TipsSerializer
    authentication_classes = [Authentication, ]
    queryset = Tips.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['index']

    def list(self, request, *args, **kwargs):
        response = super(TipsViewSet, self).list(request, *args, **kwargs)
        return BaseResponse(data=response.data)
