
'''
采集网校主页新闻数据
网址url = https://www.gdufe.edu.cn
要求：
爬取“学校新闻”、“通知公告”、“媒体广财”等三栏目上的超链接及其文本
爬取新闻图片
'''

import requests
from bs4 import BeautifulSoup
import os


# 获取网页信息
def getUrl(url):
    try:
        read = requests.get(url)  # 获取url
        read.raise_for_status()  # 状态响应 连接成功返回200 ,失败请求(非200响应)抛出异常
        read.encoding = read.apparent_encoding  # 从内容中分析响应内容编码方式
        bs = BeautifulSoup(read.text, 'html.parser')  # Http响应内容的字符串，既url对应的页面内容
        return bs
    except:
        return "连接失败"


# 获取超链接
def get_school_news(bs):
    # 创建字典dict()用于存储 文本标题与超链接
    school_news = dict()  # 创建一个空字典
    # 学校新闻
    print("学校新闻")
    # 标头文本链接
    bs1 = bs.find('div', attrs={'class': 'wrapper main1'}).find('div', attrs={'class': 'news_title_1'})
    bs1_title = bs1.a['title']
    print(bs1_title)
    bs1_href = bs1.a['href']
    print(bs1_href)
    # 加入字典中
    school_news[bs1_title] = bs1_href
    # 学校新闻超链接
    bs1_ = bs.find('div', attrs={'class': 'post post-12'}).find_all('li')
    for bs_ in bs1_:
        # 超链接的title
        bs_title = bs_.find('a')['title']
        print(bs_title)
        # 超链接
        bs_school_news = bs_.find('a')['href']
        print(bs_school_news)
        # 加入字典中
        school_news[bs_title] = bs_school_news

    return school_news


# 通知公告
def get_notice(bs):
    # 创建字典dict()用于存储 文本标题与超链接
    notice = dict()  # 创建一个空字典
    print("通知公告")
    # 标头文本链接
    bs2 = bs.find('div', attrs={'class': 'post post1 post-21'}).find('div', attrs={'class': 'news_title'})
    bs2_title = bs2.a['title']
    print(bs2_title)
    bs2_href = bs2.a['href']
    print(bs2_href)
    # 加入字典中
    notice[bs2_title] = bs2_href

    # 通知公告栏内文本链接
    bs2_ = bs.find('div', attrs={'class': 'post post1 post-211'}).find_all('li')
    # print(bs2_)
    for bs_ in bs2_:
        # 超链接的title
        bs_title = bs_.find('a')['title']
        print(bs_title)
        # 超链接
        bs_href = 'https://www.gdufe.edu.cn/' + bs_.find('a')['href']
        print(bs_href)
        # 加入字典中
        notice[bs_title] = bs_href

    return notice


# 媒体广财
def get_media_gdufe(bs):
    # 创建字典dict()用于存储 文本标题与超链接
    media_gdufe = dict()  # 创建一个空字典
    print("媒体广财")
    # 标头文本链接
    bs3 = bs.find('div', attrs={'class': 'post post1 post-22'}).find('div', attrs={'class': 'news_title'})
    bs3_title = bs3.a['title']
    print(bs3_title)
    bs3_href = bs3.a['href']
    print(bs3_href)
    # 加入字典中
    media_gdufe[bs3_title] = bs3_href

    # 通知公告栏内文本链接
    bs3_ = bs.find('div', attrs={'class': 'post post1 post-222'}).find_all('li')
    # print(bs3_)
    for bs_ in bs3_:
        # 超链接的title
        bs_title = bs_.find('a')['title']
        print(bs_title)
        # 超链接
        if 'http' not in bs_.find('a')['href']:
            bs_href = 'https://www.gdufe.edu.cn/' + bs_.find('a')['href']
            print(bs_href)
        else:
            bs_href = bs_.find('a')['href']
            print(bs_href)
        # 加入字典中
        media_gdufe[bs_title] = bs_href

    return media_gdufe


# 爬取html文本并保存下载
def getHtml(file_name,**dict):
    root = 'D:\Mylearn\web_crawler\experiment3\\' + file_name  # 保存html文本的根目录
    print(root)
    print(".......................正在下载{}文件内容.......................".format(file_name))
    for dict_key, dict_value in dict.items():
        path = root + '\\' +dict_key + '.html'  # 保存页面的绝对路径
        try:
            if not os.path.exists(root):  # 判断root路径下是否已经存在文件
                os.mkdir(root)
            if not os.path.exists(path):
                bs = getUrl(dict_value)
                fb = open(path, 'w+', encoding='utf-8')
                fb.write(bs.prettify())
                fb.close()
                print(dict_key + '.html' +"页面下载成功")
            else:
                print("文件已经存在")
        except:
            print("文件爬取失败！")


# 爬取新闻图片
def get_img(url):
    # 获取图片地址
    bs = getUrl(url)
    url_img = bs.find('div', attrs={'class': 'news_imgs'}).img['src']
    return url_img


# 获取图片保存下载
def getPic(url):
    root = "D:\Mylearn\web_crawler\experiment3\\"  # 保存图片的路径
    path = root + url.split('/')[-1]  # 获取img的文件名
    print(path)
    try:
        if not os.path.exists(root):  # 判断root路径下是否已经存在文件
            os.mkdir(root)
        if not os.path.exists(path):  # 判断path路径下是否已经存在文件
            read = requests.get(url)
            # print(read)
            with open(path, 'wb') as f:
                f.write(read.content)
                f.close()
                print(url.split('/')[-1] + "保存成功")
        else:
            print("文件已经存在！")
    except:
        print("文件爬取失败！")


# 主函数
if __name__ == '__main__':
    url = 'https://www.gdufe.edu.cn'
    bs = getUrl(url)
    # 获取图片下载地址
    # print(get_img(url))

    # 完整的图片下载地址
    url_img = url + get_img(url)
    # print(url_img)

    # 获取图片保存下载
    getPic(url_img)

    # 获取 学校新闻、通知公告、媒体广财的文本标题与链接
    # 以字典方式返回
    school_news = get_school_news(bs)
    notice = get_notice(bs)
    media_gdufe = get_media_gdufe(bs)

    # 下载html文本并保存
    # 学校新闻
    getHtml('school_news', **school_news)
    # 通知公告
    getHtml('notice', **notice)
    # 媒体广财
    getHtml('media_gdufe', **media_gdufe)