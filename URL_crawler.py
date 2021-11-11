import requests
from bs4 import BeautifulSoup
import re

class Content:
    """
    所有网页的共同基类
    """
    def __init__(self, url, title, author, content, creation_time, source, thumb_up):
        self.url = url
        self.title = title
        self.author = author
        self.content = content
        self.creation_time = creation_time
        self.source = source
        self.thumb_up = thumb_up

    def print(self):
        print("URL:{}".format(self.url))
        print("TITLE:{}".format(self.title))
        print("AUTHOR:{}".format(self.author))
        print("CONTENT:{}".format(self.content))
        print("CREATION TIME:{}".format(self.creation_time))
        print("SOURCE:{}".format(self.source))
        print("THUMB UP:\n{}".format(self.thumb_up))

class Website:
    # 标题、作者、内容、创建时间、来源、点赞量
    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, authorTag, contentTag, creation_timeTag, sourceTag, thumb_upTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl =absoluteUrl
        self.titleTag = titleTag
        self.authorTag = authorTag
        self.contentTag = contentTag
        self.creation_timeTag = creation_timeTag
        self.sourceTag = sourceTag
        self.thumb_upTag = thumb_upTag
        # print("进入website")

class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        try:
            req = requests.get(url)
            req.encoding = 'utf-8'
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parser(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            author = self.safeGet(bs, self.site.authorTag)
            content = self.safeGet(bs, self.site.contentTag)
            creation_time = self.safeGet(bs, self.site.creation_timeTag)
            source = self.safeGet(bs, self.site.sourceTag)
            thumb_up = self.safeGet(bs, self.site.thumb_upTag)
            if title !='' and author != '' and content !='' and creation_time != '' and source != '' and thumb_up !='':
                content = Content(url, title, author, content, creation_time, source, thumb_up)
                content.print()

    def crawl(self):
        """
        获取网站主页的页面链接
        :return:
        """
        bs = self.getPage(self.site.url)
        targetPages = bs.find_all('a', href = re.compile(self.site.targetPattern))
        # print(targetPages)
        for targetPage in targetPages:
            # print(targetPage)
            targetPage = targetPage.attrs['href']
            # print(targetPage)
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.url, targetPage)
                self.parser(targetPage)

if __name__ == '__main__':
    reuters = Website('lifeweek',
                      'http://www.lifeweek.com.cn/society/the-people/',
                      '(.shtml)$',
                      True,
                      'h1',
                      'h5',
                      'article p',
                      'h5',
                      'h5 a',
                      'div[class = "like mag10"] span')
    crawler = Crawler(reuters)
    # print("进入Crawler")
    crawler.crawl()