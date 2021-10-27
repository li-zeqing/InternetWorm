from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://127.0.0.1:5000/'
resp = urlopen(url)
bs = BeautifulSoup(resp.read(), 'html.parser')
print(bs.prettify())

for item in bs.next_siblings:
    print(item)