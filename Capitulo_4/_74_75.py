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