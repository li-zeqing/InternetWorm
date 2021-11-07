import requests
from bs4 import BeautifulSoup

class Content:
    """
    所有文章/网页的共同基类
    """
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        用灵活的打印函数控制结果
        :return:
        """
        print("URL:{}".format(self.url))
        print("TITLE:{}".format(self.title))
        print("BODY:\n{}".format(self.body))

class Website:
    """
    描述网页结构的信息
    """
    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Crawler:
    def getPage(self,url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        """
        用于从一个BeautifulSoup对象和一个选择器获取内容的辅助函数。
        如果选择器没有找到对象，就返回空字符串
        :param pageObj:
        :param selector:
        :return:
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, site, url):
        """
        从指定URL提取内容
        :param site:
        :param url:
        :return:
        """
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
        if title != '' and body != '':
            content = Content(url, title, body)
            content.print()

if __name__ == '__main__':
    crawler = Crawler()

    siteData = [
        [],
        [],
        [],
        []
    ]
    websites = []
    for row in siteData:
        websites.append(Website(row[0], row[1], row[2], row[3]))

    crawler.parse()