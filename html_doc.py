# -- coding:UTF-8 --
import bs4
from bs4 import BeautifulSoup

'''
2-2 爬取自建网站上的一个网页并解析
*自建网页在https://beautifulsoup.readthedocs.io/zhCN/v4.4.0/里面出现'
*输出第一个<p>标签的兄弟节点
输出第二个<p>标签的子节点,并获取<a>标签元素的内容及其href属性值
*爬虫程序中使用异常处理
'''
path = "html_doc.html"
htmlfile = open(path, 'r', encoding= 'utf-8')
bs = BeautifulSoup(htmlfile.read(),"html.parser")
# print(bs.prettify())

try:
    # print("输出第一个<p>标签的兄弟节点")
    p1_ = bs.find('p').next_siblings
    # for p1_sibling in p1_:
    #     print(p1_sibling)
    #第二个的<p>标签
    p2 = bs.find('p').next_sibling.next_sibling
    # print(p2)

    #输出第二个<p>标签的子节点
    p2_all = p2.contents
    print("输出第二个<p>标签的子节点")
    print(p2_all)

    #获取<a>标签元素的内容及其href属性值
    p2_a = p2.find_all('a')
    print("获取<a>标签元素的内容及其href属性值")
    print(p2_a)

    for child in p2.children:
        if type(child) != bs4.element.NavigableString:
            # print(type(child))
            # print(child)
            print("href属性值："+child['href'])
            print("<a>标签的内容："+child.string)


except:
    print("解析失败")