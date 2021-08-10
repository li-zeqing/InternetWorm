"""
爬取天气数据
"""
import pymysql
import requests
from bs4 import BeautifulSoup

# 连接数据库 db为数据库名称
#在此之前我们先要在crawler数据库中创建一个表weather_test用于存爬取的天气信息。
db = pymysql.connect(host="localhost", user="root", passwd="admin", db="crawler", charset='utf8')
cursor = db.cursor()


# 获取网页信息
def get_html(url):
    html = requests.get(url)
    html.encoding = 'gb2312'
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup


year = ['2017', '2018']

month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

time = [y + x for y in year for x in month]
for date in time:
    url = 'http://www.tianqihoubao.com/lishi/jinan/month/' + date + '.html'
    soup = get_html(url)
    sup = soup.find('table', attrs={'class': 'b'})
    tr = sup.find_all('tr')
    for trl in tr[1:]:
        td = trl.find_all('td')
        href = td[0].find('a')['href']  # 获取链接信息
        title = td[0].find('a')['title']  # 获取名称
        weather = td[1].get_text().replace('\r\n', '').replace(' ', '')  # 获取天气状况
        wendu = td[2].get_text().strip().replace(' ', '').replace('\r\n', '')  # 获取温度
        fengli = td[3].get_text().strip().replace(' ', '').replace('\r\n', '')  # 获取风力大小

        sql = """insert into weather_test(time_local, link, weather_type, temperature, wind_power) \
                values(%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (title, href, weather, wendu, fengli))
        db.commit()
    print("  已经爬取" + date + "数据")
db.close
print('结束')
