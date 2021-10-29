from urllib.request import urlopen
from bs4 import BeautifulSoup


def getHtml(url):
    resp = urlopen(url)
    return BeautifulSoup(resp.read(),'html.parser')

if __name__ == '__main__':
    url = 'https://baike.baidu.com/'
    bs = getHtml(url)
    print(bs.prettify())
    # print(len(bs.find_all(attrs='href')))