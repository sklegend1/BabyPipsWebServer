import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewsData,FutureData
from .serializers import NewsDataSerializer,FutureDataSerializer



from .dataminer import MiningManager


class NewsDataView(APIView):


    def search_model(self,model,parameter11=None,parameter12=None, parameter2=None, parameter3=None,
                     parameter4=None):
        query = model.objects.all()

        # Check if parameterX is provided
        if (parameter11 is not None) and (parameter12 is None):
            start_date = datetime.datetime.strptime(parameter11, "%Y-%m-%d").date()
            query = query.filter(news_date__gte=start_date)

        if (parameter11 is None) and (parameter12 is not None):
            end_date = datetime.datetime.strptime(parameter12, "%Y-%m-%d").date()
            query = query.filter(news_date__lte=end_date)

        if parameter11 and parameter12 is not None:

            start_date = datetime.datetime.strptime(parameter11, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(parameter12, "%Y-%m-%d").date()
            date_range = []
            while start_date <= end_date:
                date_range.append(start_date)
                start_date += datetime.timedelta(days=1)

            query = query.filter(news_date__in=date_range)

        if parameter2 is not None:
            query = query.filter(currency=parameter2)

        if parameter3 is not None:
            query = query.filter(description=parameter3)

        if parameter4 is not None:
            query = query.filter(impact=parameter4)

        results = query.all()

        return results

    def post(self,request):

        date_str1 = request.data.get('start_date')
        date_str2 = request.data.get('end_date')
        if date_str2 is None :
            result = self.search_model(
                NewsData,
                request.data.get('start_date'), request.data.get('end_date'), request.data.get('currency'),
                request.data.get('description'), request.data.get('impact')
            )
            serializer = NewsDataSerializer(result, many=True)
            return Response(serializer.data)

        if date_str1 is None: date_str1 = "2017-01-18"
        start_date = datetime.datetime.strptime(date_str1,"%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(date_str2, "%Y-%m-%d").date()

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        str_yesterday = str(yesterday)

        if start_date > yesterday:
            date_state = 1
            miner = MiningManager(start_date,end_date,date_state)
            miner.mine_it()
            result = self.search_model(
                FutureData,
                request.data.get('start_date'), request.data.get('end_date'), request.data.get('currency'),
                request.data.get('description'), request.data.get('impact')
            )
            serializer = FutureDataSerializer(result, many=True)
            return Response(serializer.data)

        elif end_date > yesterday:
            date_state = 2
            miner = MiningManager(start_date, end_date, date_state)
            miner.mine_it()
            result1 = self.search_model(
                NewsData,
                request.data.get('start_date'), str_yesterday , request.data.get('currency'),
                request.data.get('description'), request.data.get('impact')
            )
            result2 = self.search_model(
                FutureData,
                None, request.data.get('end_date'), request.data.get('currency'),
                request.data.get('description'), request.data.get('impact')
            )
            serializer1 = NewsDataSerializer(result1,many=True).data
            serializer2 = FutureDataSerializer(result2,many=True).data

            return Response(serializer1+serializer2)

        else:
            date_state = 3
            miner = MiningManager(start_date, end_date, date_state)
            miner.mine_it()
            result = self.search_model(
                NewsData,
                request.data.get('start_date'), request.data.get('end_date'), request.data.get('currency'),
                request.data.get('description'), request.data.get('impact')
            )
            serializer = NewsDataSerializer(result, many=True)
            return Response(serializer.data)


