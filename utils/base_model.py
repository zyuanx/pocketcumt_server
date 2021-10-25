from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, blank=True, verbose_name='修改时间')

    class Meta:
        abstract = True
