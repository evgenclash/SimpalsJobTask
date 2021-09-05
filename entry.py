from aiohttp import web
import json
import master
import nest_asyncio

# allow nested async loops
nest_asyncio.apply()


# in response to the api request is sending all the adverts with features from database
async def main(request):
    response_obj = master.getAds()

    return web.Response(text=json.dumps(response_obj), status=200)


# api request that is initializing collecting and storing adverts to the data base
def home(request):
    response_obj = 'ALl the adverts from account Johny are collected. Please go to /api as to get json data '
    master.main()
    return web.Response(text=response_obj, status=200)


app = web.Application()
app.router.add_get('/api', main)
app.router.add_get('/', home)
web.run_app(app)
