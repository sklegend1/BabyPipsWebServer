from django.db import models
from django.utils.translation import gettext_lazy as _



class NewsData(models.Model):

    news_date = models.DateField(_('date'),db_index=True)
    news_time = models.CharField(_('time'),max_length=30,db_index=True)
    currency = models.CharField(_('currency'),max_length=30, db_index=True)
    description = models.CharField(_('description'),max_length=50)
    impact = models.CharField(_('impact'),max_length=30,db_index=True)
    actual = models.CharField(_('actual'),max_length=30)
    forecast = models.CharField(_('forecast'),max_length=30)
    previous = models.CharField(_('previous'),max_length=30)

    class Meta:
        db_table = 'news_records'
        verbose_name = _('News Record')
        verbose_name_plural = _('News Record')



class FutureData(models.Model):

    news_date = models.DateField(_('date'),db_index=True)
    news_time = models.CharField(_('time'),max_length=30,db_index=True)
    currency = models.CharField(_('currency'),max_length=30, db_index=True)
    description = models.CharField(_('description'),max_length=30)
    impact = models.CharField(_('impact'),max_length=30,db_index=True)
    actual = models.CharField(_('actual'),max_length=30)
    forecast = models.CharField(_('forecast'),max_length=30)
    previous = models.CharField(_('previous'),max_length=30)

    class Meta:
        db_table = 'future_records'
        verbose_name = _('Future Record')
        verbose_name_plural = _('Future Record')




class Updates(models.Model):
    last_update=models.DateField(_('last update'),null=True)
    last_future=models.DateField(_('last future'),null=True)


