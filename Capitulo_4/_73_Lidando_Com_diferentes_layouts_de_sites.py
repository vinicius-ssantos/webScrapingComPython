"""
Este código é um web scraper que coleta o título e o corpo do texto de duas páginas da web diferentes - uma do site do Brookings Institution e outra do New York Times - usando a biblioteca BeautifulSoup para extrair informações de HTML e a biblioteca Requests para fazer solicitações HTTP.

Primeiro, a classe Content é definida com três propriedades - url, title e body - para armazenar as informações coletadas da página da web. Em seguida, há duas funções getPage e scrapeNYTimes que usam a biblioteca BeautifulSoup para extrair informações da página da web do New York Times. A função scrapeBrookings também usa a BeautifulSoup para extrair informações da página da web do Brookings Institution.

As informações coletadas para cada página são armazenadas em uma instância da classe Content e, em seguida, impressas no console usando a função print(). O resultado final é o título e o corpo do texto para as duas páginas da web.
"""

import requests
from bs4 import BeautifulSoup


class Content:

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body


def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')


def scrapeNYTimes(url):
    bs = getPage(url)
    title = bs.find("h1").text
    lines = bs.find_all("p", {"class": "css-1cy1v93"})
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)


def scrapeBrookings(url):
    bs = getPage(url)
    title = bs.find("h1").text
    body = bs.find("div", {"class", "post-body"}).text
    return Content(url, title, body)


url = 'https://www.brookings.edu/blog/future-development/2018/01/26/delivering-inclusive-urban-access-3-uncomfortable-truths/'
content = scrapeBrookings(url)
print('Title: {}'.format(content.title))
print('URL: {}\n'.format(content.url))
print(content.body)

url = 'https://www.nytimes.com/2018/01/25/opinion/sunday/silicon-valley-immortality.html'
content = scrapeNYTimes(url)
print('Title: {}'.format(content.title))
print('URL: {}\n'.format(content.url))
print(content.body)
