import asyncio
import math
from time import sleep
import requests
import aiohttp


class SimpalsApiClient:
    endPoint = 'https://partners-api.999.md/adverts'
    auth = ('apuUo-UF6yhfoNVVTKWrb5Z8ecru', '')
    page_size = 3

    def __init__(self):
        self.adverts = {'adverts': []}
        advertsResponse = self.http()
        self.advertsFromHttp = advertsResponse.json()
        self.page_size = self.advertsFromHttp['page_size']

    # used for the first request to server
    def http(self):
        return requests.get(f'{self.endPoint}?page_size={self.page_size}', auth=self.auth)

    # this method is requesting and returning the features of an advert
    async def getAdvertsFeaturesFromServer(self, session, id):
        headers = {'content-type': 'application/json'}
        auth = aiohttp.BasicAuth('apuUo-UF6yhfoNVVTKWrb5Z8ecru', '')
        features = '429 server status'

        # while loop is avoiding the 429 server status
        while features == '429 server status':
            async with session.get(f'{self.endPoint}/{id}', auth=auth, headers=headers) as response:
                try:
                    features = await response.json()
                except:
                    # sleep is avoiding too many requests response from server
                    sleep(0.1)
                    features = '429 server status'
        return features

    # this method is requesting and returning the advert
    async def getAdvertsFromServer(self, session, page):
        auth = aiohttp.BasicAuth('apuUo-UF6yhfoNVVTKWrb5Z8ecru', '')
        advertsPerPage = '429 server status'

        while advertsPerPage == '429 server status':
            async with session.get(f'{self.endPoint}?page_size={self.page_size}&page={page + 1}',
                                   auth=auth) as response:
                try:
                    advertsPerPage = await response.json()
                except:
                    sleep(0.1)
                    advertsPerPage = '429 server status'

        return advertsPerPage

    # it is collecting asynchronous the adverts
    async def addAdverts(self):

        async with aiohttp.ClientSession() as session:
            tasks1 = []

            pages = math.ceil(self.advertsFromHttp['total'] / self.page_size)
            if pages > 1:

                for page in range(pages):
                    task = asyncio.ensure_future(self.getAdverts(session, page))
                    tasks1.append(task)

                await asyncio.gather(*tasks1)

    # collecting each advert
    async def getAdverts(self, session, page):
        advertsPerPage = await self.getAdvertsFromServer(session, page)

        for advert in advertsPerPage['adverts']:

            # adding each advert from the page i to adverts
            self.adverts['adverts'].append(advert)

    # main method for collecting the features
    async def addFeatures(self):
        tasks2 = []
        async with aiohttp.ClientSession() as session:
            
            for advert in self.adverts['adverts']:
                tasks = asyncio.ensure_future(self.getAdvertsFeatures(session, advert['id'], advert))
                tasks2.append(tasks)

            await asyncio.gather(*tasks2)

    # it is adding the features of adverts to each advert
    async def getAdvertsFeatures(self, session, id, advert):
        features = await self.getAdvertsFeaturesFromServer(session, id)

        advert['features'] = features

    # it is initializing the async loops for collecting adverts and features
    def getAdvertsAsync(self):
        asyncio.run(self.addAdverts())
        asyncio.run(self.addFeatures())

        return self.adverts
