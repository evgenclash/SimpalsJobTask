import requests
from bs4 import BeautifulSoup


class Currency:

    # parsing the bnm exchange rate when initialized and storing them to exchangeRate attribute
    def __init__(self):
        exchangeRate = {}
        response = requests.get('https://www.bnm.md/ro')
        soup = BeautifulSoup(response.content, 'html.parser')
        currencies = soup.find_all('span', class_="currency")

        for currency in currencies:
            value = currency.find_next('span').text
            exchangeRate[str.lower(currency.text)] = value
        self.exchangeRate = exchangeRate

    # checking if unit is usd or eur and sending the value to a method that is converting them to mdl
    def currencyCheck(self, adverts):

        for advert in adverts['adverts']:
            currency = advert['features']['price']['unit']

            if currency == 'eur' or currency == 'usd':

                # change unit to mdl
                advert['features']['price']['unit'] = 'mdl'
                value = advert['features']['price']['value']

                # change the value to mdl by calling currencyExchange method
                advert['features']['price']['value'] = self.currencyExchange(currency, value)

        return adverts

    # checking the currency if it eur or usd and converting to mdl
    def currencyExchange(self, currency, value):

        if currency == 'eur':
            return int(value * float(self.exchangeRate['eur']))

        if currency == 'usd':
            return int(value * float(self.exchangeRate['usd']))
