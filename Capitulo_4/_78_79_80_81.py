"""
Esse código é um web crawler que busca por tópicos em vários sites e registra informações
sobre as páginas encontradas.

A classe Content representa uma página encontrada, com informações como o tópico, URL,
título e corpo do texto. A classe Website contém informações sobre a estrutura do site,
como a URL base, a URL de pesquisa, a lista de resultados, etc. A classe Crawler contém
métodos para buscar páginas web, extrair informações e pesquisar por tópicos em um dado
site.

O código começa criando uma lista de objetos Website para cada um dos sites que serão
pesquisados, com suas respectivas informações de busca. Em seguida, para cada tópico,
o código percorre a lista de sites e utiliza o método search do objeto Crawler para
buscar páginas relevantes para o tópico em cada site. A cada página encontrada,
uma instância de Content é criada e suas informações são impressas na tela.

"""
import requests
from bs4 import BeautifulSoup


class Content:
    """Classe base comum para todos os artigos/páginas"""

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """Uma função flexível de exibição controla a saída"""

        print("New Article found for topic: {}".format(self.topic))
        print('Title: {}'.format(self.title))
        print('BODY: \n{}'.format(self.body))
        print('URL: {}'.format(self.url))


class Website:
    """Contém informações sobre a estrutura do site"""

    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ""

    def search(self, topic, site):
        """Pesquise um dado site em busca de um dado tópico e registra todas as páginas encontradas"""
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs["href"]
            # Verifica se é um URL relativo ou absoluto
            if (site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print("Something was wrong with that page or URL. Skipping!")
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()


crawler = Crawler()

siteData = \
    [['O\'Reilly Media', 'http://oreilly.com', 'https://ssearch.oreilly.com/?q=', 'article.product-result', 'p.title a',
      True, 'h1', 'section#product-description'],
     ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=', 'div.search-result-content',
      'h3.search-result-title a', False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
     ['Brookings', 'http://www.brookings.edu', 'https://www.brookings.edu/search/?s=', 'div.list-content article',
      'h4.title a', True, 'h1', 'div.post-body']]
sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    topics = ['python', 'data science']
    for topic in topics:
        print("GETTING INFO ABOUT: " + topic)
        for targetSite in sites:
            crawler.search(topic, targetSite)
