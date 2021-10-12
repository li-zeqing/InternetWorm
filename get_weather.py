'''
爬取某城市的天气
url = http://www.weather.com.cn/weather/101280601.shtml
爬取信息包括 xx日(周几) 多云 日温度范围  风向 xx级 共5项
'''
import requests
from bs4 import BeautifulSoup

# 获取网页信息
def get_html(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    bs = BeautifulSoup(html.text,'html.parser')
    return bs

# 获取网页中7天天气信息
url = 'http://www.weather.com.cn/weather/101280601.shtml'
bs = get_html(url)
# print(bs.prettify())
bs = bs.find('ul', attrs = {'class':'t clearfix'})
tr = bs.find_all('li')
# print(tr[0])
# print(type(tr[0]))
# print(tr.prettify())
for trl in tr:
    # 获取日期
    data_ = trl.find('h1').text
    # print(data_)
    # 获取天气预报
    weather_ = trl.find('p').text
    # print(weather_)
    # 获取温度
    temperature_ = trl.find('p',attrs = {'class':'tem'}).text.replace('\n','')
    # print(temperature_)
    # 获取风向
    wind_ = trl.find('p',attrs = {'class':'win'}).span['title']
    # print(wind_)
    # 获取风的级数
    wind_scale = trl.find('p',attrs = {'class':'win'}).text.replace('\n','')
    # print(wind_scale)
     #打印输出
    print("{} {} {} {} {}".format(data_,weather_,temperature_,wind_,wind_scale))