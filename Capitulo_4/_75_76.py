"""
Este código é um exemplo de um rastreador da web que pode extrair o título e o corpo do texto de uma página da web para vários sites de notícias. O código começa definindo uma classe Content que é usada para representar o título, o corpo e o URL de uma página da web. Em seguida, a classe Website é definida para representar as informações necessárias para acessar o conteúdo de um site específico, incluindo o nome do site, o URL da página inicial, o nome do elemento que contém o título e o nome do elemento que contém o corpo do texto.

A classe Crawler é responsável por extrair o conteúdo da página da web. Ela define um método getPage para recuperar o conteúdo HTML de uma página da web, e um método safeGet para extrair o texto de um elemento específico de uma página da web. O método parse recebe um objeto Website e uma URL e usa o método getPage para baixar o conteúdo HTML da página da web. Em seguida, ele usa o nome dos elementos do site para recuperar o título e o corpo da página da web e, se as informações foram encontradas, cria um objeto Content e chama o método print para exibir o título, URL e corpo da página da web.

Por fim, o código define uma lista de sites de notícias e seus URLs, cria objetos Website para cada um deles e chama o método parse para extrair o conteúdo de quatro páginas da web diferentes. O resultado será a exibição do título, URL e corpo de cada página da web no console.
"""

import requests
from bs4 import BeautifulSoup

class Content:
    """
    Classe-base comum para todos os artigos/páginas
    """

    def __init__(self,url,title,body):
        self.url=url
        self.title=title
        self.body=body

    def print(self):
        """
        Uma função flexível de exibição controla a saída
        """
        print('Title: {}'.format(self.title))
        print('URL: {}\n'.format(self.url))
        print('BODY: \n{}'.format(self.body))

class website:
    """
    Contém informaçõoes sobre a estrutura do site
    """

    def __init__(self,name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.title = titleTag
        self.body = bodyTag

class Crawler:
    def getPage(url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        """
        Função utilitária usada para obter uma string de conteúdo de um objeto BeautifulSoup
        e um seletor, Devolve uma string vazia caso nenhum objeto seja encotrado para o dado
        seletor
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''


    def parse(self,site,url):
        """
        Extra conteúdo de um dado URL de página
        """

        bs = self.getPage(url)
        if bs is not None:
            title = self.getPage(bs,site.titleTag)
            body = self.safeGet(bs,site.bodyTag)
            if title != '' and  body != '':
                content = Content(url,title,body)
                content.print()


crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com', 'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com', 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu', 'h1', 'div.post-body'],
    ['New York Times', 'http://nytimes.com', 'h1', 'div.StoryBodyCompanionColumn div p']
]
websites = []
for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3]))

crawler.parse(websites[0], 'http://shop.oreilly.com/product/0636920028154.do')
crawler.parse(
    websites[1], 'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(
    websites[2],
    'https://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')
crawler.parse(
    websites[3],
    'https://www.nytimes.com/2018/01/28/business/energy-environment/oil-boom.html')