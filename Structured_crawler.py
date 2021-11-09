import requests
from bs4 import BeautifulSoup

class Content:
    """
    所有文章 网页的共同基类
    """
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print("New article found for topic:{}".format(self.topic))
        print("URL:{}".format(self.url))
        print("TITLE:{}".format(self.title))
        print("BODY:\n{}".format(self.body))




class Website:
    """
    描述网站结构信息
    """
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
    # 获取页面
    def getPage(self, url):
        try:
            headers = {
            'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
            }
            req = requests.get(url, headers = headers)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ""

    def search(self, topic, site):
        """
        根据主题搜索网站并记录所有找到的页面
        :param topic:
        :param site:
        :return:
        """

        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            # 检查一下是否为相对URL还是绝对URL
            if (site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print("Something was wrong with that page or URL.Skipping!")
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print()
if __name__ == '__main__':
    crawler = Crawler()

    siteData = ['dangdang', 'https://www.dangdang.com', 'http://search.dangdang.com/?key=', 'div#search_nature_rg > ul', 'li a', False, 'div.messbox_info span.t1 > a', 'div.messbox_info span[dd_name = "出版社"] > a']

    sites = []

    # for row in siteData:
    #     print(row)
    #     print(len(row))
    row = siteData
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    topics = ['python']
    for topic in topics:
        print("GETTING INFO ABOUT:" + topic)
        for targetSite in sites:
            crawler.search(topic, targetSite)
