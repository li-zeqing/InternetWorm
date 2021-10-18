# -- coding:UTF-8 --
from urllib.request import urlopen
from urllib.error import HTTPError

import bs4
from bs4 import BeautifulSoup
import requests

# 下载页面内容
def getHtml(url):
    read = requests.get(url)
    bs = BeautifulSoup(read.text,'html.parser')
    path = 'BeautifulSoup_zh_CN.html'   #保存页面的相对路径
    fb = open(path, 'w+', encoding='UTF-8')
    fb.write(bs.prettify())
    fb.close()

def getTag(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html,'html.parser')
        # print(bs)
        Tag1 = bs.p.next_sibling
        return Tag1
    except AttributeError as e:
        return None


if __name__ == '__main__':
    url = 'https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/'
    # getHtml(url)    #下载页面
    bs2 = BeautifulSoup(urlopen(url), 'html.parser')
    # 第一个<p>节点在<div class="section" id="beautiful-soup-4-4-0">之内

    # print(bs2.p.prettify())
    #找到符合条件的第一个<p>标签
    first_p = bs2.find('div',attrs={"class": "section","id":"beautiful-soup-4-4-0"}).p
    # print(type(first_p))
    #第一个<p>标签的兄弟节点
    first_p_sibling = first_p.next_sibling.next_sibling
    print("输出第一个<p>标签的兄弟结点：")
    print(first_p_sibling)
    #第二个<p>标签的所有兄弟节点
    first_p_sibling_all = first_p_sibling.next_siblings
    print("输出第二个<p>标签的兄弟结点：")
    for tag_sibling in first_p_sibling_all:
        if type(tag_sibling) == bs4.element.NavigableString:
            pass
        elif tag_sibling.find('a') == None:
            pass
        else:
            print("<a>标签元素内容")
            print(tag_sibling.find('a'))
            # print(type(tag_sibling.find('a')))
            print("<a>标签的href与内容")
            print(tag_sibling.find('a')['href'])
            print(tag_sibling.find('a').string)
            print("++++++++++++++++++分隔线++++++++++++++++++++++")


