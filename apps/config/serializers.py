from apps.config.models import Carousel, Tips
from utils.base_serializers import BaseModelSerializer


class TipsSerializer(BaseModelSerializer):
    """
    贴士列表序列化
    """

    class Meta:
        model = Tips
        fields = '__all__'


class CarouselSerializer(BaseModelSerializer):
    """
    轮播图列表序列化
    """

    class Meta:
        model = Carousel
        fields = '__all__'
