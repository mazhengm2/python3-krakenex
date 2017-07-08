#get the real time exchange rate from Fixer.io
import requests


def get_USD2CNY():
    return requests.get('http://api.fixer.io/latest?base=USD&symbols=CNY').json()['rates']['CNY']
def get_CNY2USD():
    return requests.get('http://api.fixer.io/latest?base=CNY&symbols=USD').json()['rates']['USD']

#print(get_CNY2USD(),get_USD2CNY())