from pymongo import MongoClient
from Currency import *
from client.SimpalsApiClient import *


class MongoDB:

    def __init__(self):
        myclient = MongoClient(
            "mongodb+srv://root:root@cluster0.tthim.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = myclient["simpals"]
        collection = db["adverts"]
        self.collection = collection
        exchange = Currency()
        self.exchange = exchange

    # writing all the adverts to the db
    def writeInDB(self, adverts):
        adverts = self.exchange.currencyCheck(adverts)

        for i in range(len(adverts['adverts'])):
            self.collection.insert_one(adverts['adverts'][i])

    # used as to clear the database
    def deleteAll(self):
        self.collection.delete_many({})

    def checkForUpdates(self):
        adverts = SimpalsApiClient()
        ids = []

        # iterating through each advert from api
        advertsFromApi = adverts.getAdvertsAsync()
        for i in range(len(advertsFromApi['adverts'])):
            id = advertsFromApi['adverts'][i]['id']
            advertFromDB = self.collection.find_one({"id": id})
            ids.append(id)

            # check if it is already in the DB
            if advertFromDB == None:
                print('added to db:' + str(id))
                self.collection.insert_one(advertsFromApi['adverts'][i])

            # check if there have been made any changes
            elif advertsFromApi['adverts'][i]['republished'] != advertFromDB['republished']:
                self.collection.replace_one({"id": id}, advertsFromApi['adverts'][i])
                print('have updated')

        #     iterating through each advert from db as to check if there are any adverts that are deleted from the simpals server and deletes them if needed
        advertsFromDB = self.collection.find({})
        for advertFromDB in advertsFromDB:
            if advertFromDB['id'] not in ids:
                print('deleted object')
                self.collection.delete_one({'id': advertFromDB['id']})

    # this methods takes all the adverts from the database and return them
    def getAllAdverts(self):
        ads = self.collection.find({})
        adverts = {'adverts': []}

        for ad in ads:
            del ad['_id']
            adverts['adverts'].append(ad)

        return adverts
