import datetime

from .models import NewsData,FutureData,Updates
from .serializers import *
from .BabyPipsMine import BPCollector



class MiningManager():
    def __init__(self,start_date,end_date,date_state):
        self.start_date = start_date
        self.end_date = end_date
        self.yesterday = datetime.date.today()-datetime.timedelta(days=1)
        self.date_state = date_state


    def create_data(self,model,start_date,end_date):

        BPCollector.start_date = start_date
        BPCollector.end_date = end_date
        BPCollector.start_week = start_date.isocalendar()[1]
        if BPCollector.start_week == 53: BPCollector.start_week = 1
        if BPCollector.end_week == 53: BPCollector.end_week = 1
        BPCollector.end_week = end_date.isocalendar()[1]

        dict1 = BPCollector.collecting_babypips_data()


        for i in range(BPCollector.records_count):

            if dict1['data'][i][0]<start_date :
                continue

            if dict1['data'][i][0]>end_date :
                break



            model.objects.create(news_date=dict1['data'][i][0]
                                            ,news_time=dict1['data'][i][1],
                                            currency=dict1['data'][i][2],description=dict1['data'][i][3],
                                            impact=dict1['data'][i][4],actual=dict1['data'][i][5]
                                            ,forecast=dict1['data'][i][6], previous=dict1['data'][i][7])

    def update_database(self):
        first_date = datetime.date(2017,1,17)

        try :

            print(Updates.objects.values_list("last_update")[0][0])
            last_update = Updates.objects.values_list("last_update")[0][0]
        except :
            Updates.objects.create(pk=1 , last_update=first_date,last_future=self.yesterday)
            print(Updates.objects.values_list("last_update")[0][0])
            last_update = Updates.objects.values_list("last_update")[0][0]
        try :
            serializer = NewsData.objects.filter(news_date__gt=last_update).order_by("-news_date")
            last_record= NewsDataSerializer(serializer,many=True).data
            last_update = datetime.datetime.strptime(last_record[0]["news_date"], "%Y-%m-%d").date()
            Updates.objects.filter(pk=1).update(last_update=last_update)
            print("last update : " ,last_update)
        except : pass
        if last_update >= self.yesterday : return
        try  :
            self.create_data(NewsData,last_update+datetime.timedelta(days=1),self.yesterday)
            serializer = NewsData.objects.all().order_by("-news_date")
            last_record = NewsDataSerializer(serializer, many=True).data
            last_update = datetime.datetime.strptime(last_record[0]["news_date"], "%Y-%m-%d").date()
            Updates.objects.filter(pk=1).update(last_update=last_update)
            FutureData.objects.filter(news_date__lt= datetime.date.today()).delete()

        except Exception as err:
            print(err)

    def update_future (self):

        last_future = Updates.objects.values_list("last_future")[0][0]
        try:
            serializer = FutureData.objects.filter(news_date__gt=last_future).order_by("-news_date")
            last_record = FutureDataSerializer(serializer, many=True).data
            print("correct future :", last_record[0]["news_date"])
            last_future = datetime.datetime.strptime(last_record[0]["news_date"], "%Y-%m-%d").date()
            Updates.objects.filter(pk=1).update(last_future=last_future)
            print("last future : ", last_future)
        except:
            pass

        if self.end_date > last_future:
            try:
                self.create_data(FutureData, last_future + datetime.timedelta(days=1), self.end_date)
                serializer = FutureData.objects.all().order_by("-news_date")
                last_record = FutureDataSerializer(serializer, many=True).data
                last_future = datetime.datetime.strptime(last_record[0]["news_date"], "%Y-%m-%d").date()
                Updates.objects.filter(pk=1).update(last_future=last_future)
            except Exception as err:
                print(err)






    def mine_it (self):

        self.update_database()

        if self.date_state in [1,2]:
            self.update_future()

