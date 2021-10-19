# -- coding:UTF-8 --
from urllib.request import urlopen

import bs4
from bs4 import BeautifulSoup
'''
2-2 爬取自建网站上的一个网页并解析
*自建网页在https://beautifulsoup.readthedocs.io/zhCN/v4.4.0/里面出现'
*输出第一个<p>标签的兄弟节点
输出第二个<p>标签的兄弟节点,并获取<a>标签元素的内容及其href属性值
*爬虫程序中使用异常处理
'''
url = 'https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/'

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