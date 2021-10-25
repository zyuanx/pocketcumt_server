from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.config.models import Carousel, Tips


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe('<img src="%s" width="100px;" />' % (obj.image.url,))

    show_img.short_description = '配图'
    list_display = ('title', 'carousel_type', 'status', 'index', 'show_img', 'modified_time',)
    ordering = ['index', ]


@admin.register(Tips)
class TipsAdmin(admin.ModelAdmin):
    def show_img(self, obj):
        return mark_safe('<img src="%s" width="100px;" />' % (obj.image.url,))

    show_img.short_description = '配图'
    list_display = ('title', 'status', 'index', 'show_img', 'modified_time',)
    ordering = ['index', ]
