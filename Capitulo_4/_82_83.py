import requests
from bs4 import BeautifulSoup


class Website:

    def __init__(self, name, url, targetPattern, absoluteUrl):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl


class Content:
    """Classe base comum para todos os artigos/páginas"""

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """Uma função flexível de exibição controla a saída"""

        print('URL: {}'.format(self.url))
        print('Title: {}'.format(self.title))
        print('BODY: \n{}'.format(self.body))


class Crawler:
    def __int__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')


    def safeGet(self,pageObj,selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) >0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self,url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs,self.site.titleTag)
            body = self.safeGet(bs,self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url,title,body)
                content.print()
