from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(NewsData)
class NewsDataAdmin(admin.ModelAdmin):
    list_display =['news_date','news_time','currency','description','impact','actual','forecast','previous']
    list_filter = ['news_date','currency','impact']
    date_hierarchy = 'news_date'


@admin.register(FutureData)
class FutureDataAdmin(admin.ModelAdmin):
    list_display =['news_date','news_time','currency','description','impact','actual','forecast','previous']
    list_filter = ['news_date','currency','impact']
    date_hierarchy = 'news_date'