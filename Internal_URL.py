from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
from queue import Queue

# 队列存内链 列表存所以的内链
internalQueue = Queue(maxsize=0)
internalLinks = set()

# 存储所有的外链
externalLinks = set()

# 获取页面
def getHtml(url):
    try:
        html = urlopen(url)
        bs_ = BeautifulSoup(html,'html.parser')
        # print(type(bs_))
        return bs_
    except HTTPError as e:
        print(url)
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


# 获取页面中所以内链的列表
def getInternalLinks(bs, includeUrl):
    # includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme, urlparse(includeUrl).netloc)
    # print("内链"+includeUrl)
    if (includeUrl.endswith('/')):
        includeUrl = includeUrl[:-1]
    # 找出所有以'/'开头的链接
    for link in bs.find_all('a', href = re.compile('^(/|.*'+urlparse(includeUrl).netloc+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith('/')):
                    if (includeUrl.split('/')[-1][-5:] == '.html'):
                        includeUrl = '/'.join(includeUrl.split('/')[:-1])
                    internalLinks.add(includeUrl+link.attrs['href'])
                    internalQueue.put(includeUrl+link.attrs['href'])
                        # print(includeUrl+link.attrs['href'])
                else:
                    internalLinks.add(link.attrs['href'])
                    internalQueue.put(link.attrs['href'])
                    # print(link.attrs['href'])

    return 0

# 获取页面中所有外链列表
def getExternalLinks(bs, excludeUrl):
    # 找出所有以http或www开头且不包含当前URL的链接
    for link in bs.find_all('a', href = re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.add(link.attrs['href'])
                # print(link.attrs['href'])

    return 0

def getInternalLink_BFS(startingPage):
    bs = getHtml(startingPage)
    while(type(bs).__name__ != 'BeautifulSoup'):
        if not internalQueue.empty(): # 判断队列是否为空
            startingPage = internalQueue.get()  # 队头元素出队
            bs = getHtml(startingPage)
        # else:
        print("内链队列已经为空")
        break
    if type(bs).__name__ == 'BeautifulSoup':    #当bs对象为BeautifulSoup时才能执行以下操作
        # 获取次页面的所有外链
        getExternalLinks(bs, urlparse(startingPage).netloc)

        # 获取所有的内链 并入队
        getInternalLinks(bs,startingPage)
        if not internalQueue.empty():
            a = internalQueue.get() # 获取队头元素
            # print("队头的内链是"+a)
            return getInternalLink_BFS(a)   #递归调研广度优先搜索函数
    return 0

if __name__ == '__main__':
    startingPage = 'https://www.oreilly.com'
    getInternalLink_BFS(startingPage)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("外链数量:{}".format(len(externalLinks)))
    print("内链数量:{}".format(len(internalLinks)))
    print("打印所有的外链：")
    for externalLink in externalLinks:
        print(externalLink)