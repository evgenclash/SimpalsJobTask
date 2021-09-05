# SimpalsJobTask
This is a test task for Job at Simpals
It is requesting the adverts from account Johny164 using rest API of Simpals and is storing all the data to MongoDB
In total I have spent around 30 hours all together with studiyng new frameworks and writing the code for the task


Instructions how to run and how does the application work
open and run entry.py file as to start
"http://0.0.0.0:8080/" the api request on this url will initiate the process of collecting the adverts and the features of each advert and storing them to the database
"http://0.0.0.0:8080/api" this api request will return all the adverts stored in the database in json format 
in pictures file you can see the outputs.

master file contains 2 functions, 
->main() is initializing all the proccesses(collecting and storing adverts to database)

->getAds() is returning all the data stored in the database
1)is creating a MongoDB object
2)is requesting all the adverts from the database
3)returns all the adverts from database

in main()
adverts = SimpalsApiClient()
is creating a SimpalsApiClient object and is runing the __init__() method of SimpalsApiClient

->__init__()
1)creating an attribute that will store in the futures al the adverts and features
2)making first request to simpals server as to count later number of pages 

-->getAdvertsAsync() stored in file SimpalsApiClient is collecting adverts by running 
asyncio.run(self.addAdverts())

--->addAdverts() 
1)is creating a async Session
2)checking the number of page (by default Sipamls rest api is returning page_size=30 but I have set it to 3 as to avoid the problem that can appear in the future when Johny164 has more than 30 adverts)
3)if there is more than 1 pages we are iterating through all pages and asynchronously sending the requests to the Sipamls rest api by calling method 

---->getAdverts() and save the tasks created
3.1)gets all the adverts from the page by calling 

----->getAdvertsFromServer()
3.1.1) while loop is avoiding 429 server status (too many requests) when we get 429 server status we let the code to wait for 0.1 sec
3.1.2)if as response to the requests we get json content-type we return the advertsPerPage we got from server
3.2)iterating through all adverts we got at step 3.1 and appending each advert to the adverts['adverts'] attribute that is of type dict and was created when SimpalsApiClient is initialized
4)gather all the task 

and then asyncio.run(self.addFeatures()) starts the loop of collecting features of each advert
--->addFeatures()
1)is creating a async Session
2)iterationg through all the adverts that was collected previously and asynchronously sending the requests to the Sipamls rest api by calling method 
---->getAdvertsFeatures()
2.1) getAdvertsFeatures() is sending request to Simpals server and gets the features of the advert by calling method
----->getAdvertsFeaturesFromServer()
2.1.1)while loop is avoiding 429 server status (too many requests) when we get 429 server status we let the code to wait for 0.1 sec
2.1.2)if as response to the requests we get json content-type we return the advertsPerPage we got from server
2.2)appending the features to the advert it is related to
3)gather all the tasks


mongo = MongoDB() in main() is initializing MongoDB object
1)is created mongoClient and the collection where all the data will be stored
2)exchange = Currency() is creating an object that will check and convert the unit price and value before writing adverts to the database
Currency when initialized is:
2.1)parsing the bnm site
2.2)extracting all the currencies and rates
2.3)returning the exchange rates from bnm 

mongo.deleteAll() from main() is deleting all the adverts from DB

mongo.writeInDB(advertsWithFeatures) is writing all the adverts in the DB
1)first of all it is calling the method currencyCheck() from exchange object
--->exchange.currencyCheck()
1.1)iterating through all the adverts
2.1)checkig if unit is eur or usd, if yes then unit is changed to mdl and value is sent to 
->currencyExchange() method
2.1.1) if currency = eur value is multiplied with the currency exchange rate of eur 
2.1.2) if currency = usd value is multiplied with the currency exchange rate of usd 
2.2) storing the new value
2.3)returning all the adverts with updated unit and value (mdl)
3) iterating through all the adverts and inserting them to the DB


mongo.checkForUpdates() from main() is checking for the updates 
1)creating new SimpalsApiClient object
2)call the getAdvertsAsync() method from SimpalsApiClient class as to get all the adverts from server
3)iterate through all the adverts we got 
4)check if there is an advert with the same id in the DB
5)if is none then add the advert to DB
6)if republished time has chenged then we updata the advert in the DB
7)check if there is any advert in the database that is deleted from the simpals server











