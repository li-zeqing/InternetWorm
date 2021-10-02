# -- coding:UTF-8 --
import requests
from bs4 import BeautifulSoup
import os

'''
思路：
    下载页面文本
    获取图片地址
    爬取图片并保存
'''


# 获取网址
def getUrl(url):
    try:
        read = requests.get(url)  # 获取url
        read.raise_for_status()  # 状态响应 返回200连接成功
        read.encoding = read.apparent_encoding  # 从内容中分析响应内容编码方式
        return read.text  # Http响应内容的字符串，既url对应的页面内容
    except:
        return "连接失败"


# 获取图片地址并保存下载
def getPic(html):
    soup = BeautifulSoup(html, "html.parser")
    # 通过分析页面内容 查找img标签
    all_img = soup.find_all('img')  # 查找所以的img标签
    for img in all_img:
        src = img['src']  # 获取img标签里的src内容
        img_url = src
        print(img_url)
        root = "D:/Mylearn/InternetWorm/text_Flask/static/images/"  # 保存图片的路径
        path = root + img_url.split('/')[-1]  # 获取img的文件名
        print(path)
        try:
            # if not os.path.exists(root):
            #     os.mkdir(root)
            if not os.path.exists(path):
                read = requests.get(img_url)
                with open(path, 'wb') as f:
                    f.write(read.content)
                    f.close()
                    print(img_url.split('/')[-1] + "保存成功")
            else:
                print("文件已经存在！")
        except:
            print("文件爬取失败！")


# 主函数
if __name__ == '__main__':
    html_url = getUrl("http://pythonscraping.com/pages/page3.html")
    getPic(html_url)
