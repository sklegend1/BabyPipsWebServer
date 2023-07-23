from rest_framework import serializers
from .models import NewsData,FutureData,Updates

class NewsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsData
        fields = ('news_date','news_time','currency','description','impact','actual','forecast','previous')

class FutureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureData
        fields = ('news_date','news_time','currency','description','impact','actual','forecast','previous')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Updates
        fields = ('last_update','last_future')

