from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import bs4


def getHtml(url):
    resp = urlopen(url)
    bs = BeautifulSoup(resp.read(),'html.parser')
    print(type(bs))
    print(type(bs).__name__ )

def getParse(url):
    parse = urlparse(url)
    print(parse)
    print(type(parse))
    print(parse.scheme)
    print(parse.netloc)
    print(parse.path)
    print(type(parse.scheme))

if __name__ == '__main__':
    url1 = 'https://www.oreilly.com'
    url2 = 'https://www.oreilly.com/online-learning/government.html'
    url3 = 'https://www.oreilly.com/online-learning/support/content.html'
    print(url3.split('/')[-1][-5:] == '.html')
    print('/'.join(url3.split('/')[:-1]))
    bs = getHtml(url1)
    # getParse(url2)
    getParse(url3)
    # print(bs.prettify())
    # print(len(bs.find_all(attrs='href')))