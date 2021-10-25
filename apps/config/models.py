from django.db import models

from utils.base_model import BaseModel
from utils.storage import ImageStorage


class Carousel(BaseModel):
    """
    轮播图
    """
    STATUS_ITEMS = (
        (0, '不显示'),
        (1, '显示'),
    )
    TYPE_ITEMS = (
        (0, '图片'),
        (1, '推文'),
    )
    title = models.CharField(max_length=32, verbose_name='标题')
    web = models.URLField(max_length=255, null=True, blank=True, verbose_name='推文链接')
    image = models.ImageField(upload_to='carousel/%Y/%m/%d', default='carousel/default.jpg', blank=True,
                              storage=ImageStorage(), verbose_name='图片', )
    status = models.SmallIntegerField(choices=STATUS_ITEMS, default=1, verbose_name='状态')
    carousel_type = models.SmallIntegerField(choices=TYPE_ITEMS, default=0, verbose_name='类型')
    index = models.SmallIntegerField(default=1, verbose_name='索引顺序')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name


class Tips(BaseModel):
    STATUS_ITEMS = (
        (0, '不显示'),
        (1, '显示'),
    )
    title = models.CharField(max_length=32, verbose_name='标题')
    image = models.ImageField(upload_to='tips/%Y/%m/%d', default='tips/default.jpg', blank=True,
                              storage=ImageStorage(), verbose_name='图片', )
    status = models.SmallIntegerField(choices=STATUS_ITEMS, default=1, verbose_name='状态')
    index = models.CharField(max_length=32, verbose_name='索引')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '贴士'
        verbose_name_plural = verbose_name
