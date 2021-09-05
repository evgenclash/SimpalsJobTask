from MongoDB import *
from client.SimpalsApiClient import *
import time


# it is collecting from SimpalsApiClient the adverts and storing, updating them to MongoDB
def main():
    star_time = time.time()
    adverts = SimpalsApiClient()
    # adding the features to each advert
    advertsWithFeatures = adverts.getAdvertsAsync()

    mongo = MongoDB()

    # clear all the data in database
    mongo.deleteAll()

    # write in the DB all the adverts and features
    mongo.writeInDB(advertsWithFeatures)

    # check for updates in adverts for Johny account and write them in DB
    mongo.checkForUpdates()

    total_time = time.time() - star_time

    print(total_time)


# main()

# it it called for returning adverts as response to Api request
def getAds():
    mongo = MongoDB()
    ads = mongo.getAllAdverts()

    return ads
