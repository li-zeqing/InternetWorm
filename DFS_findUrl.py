from urllib.request import urlopen
from bs4 import BeautifulSoup

# 深度优先搜索
# 创建栈用于存储页面链接
class StackBrowser(object):
    def __init__(self, length = 20):
        self.item = []  #初始化，创建一个list
        self.length = length

    def push(self, value): #tes 入栈
        if self.is_full():
            return None
        else:
            self.item.append(value)

    def pop(self):  # 出栈
        if self.is_empty():
            return None
        self.item.pop()

    def top(self):
        if self.is_empty():
            return None
        return self.item[-1]

    def is_empty(self):
        return len(self.item) == 0

    def is_full(self):
        if len(self.item) >= self.length:
            return True

    def size(self):
        return len(self.item)

    def show_stack(self):
        print(self.item)

# 解析网页
def getHtml(url):
    resp = urlopen(url)
    bs = BeautifulSoup(resp.read(), 'html.parser')
    return bs


if __name__ == '__main__':
    # 创建一个栈
    stack = StackBrowser()
    url = 'http://134.175.175.191/ScrapyStrategy/books.html'
    url_top = 'http://134.175.175.191'
    bs = getHtml(url)
    print(bs.h3.get_text())
    # print(bs_a)
    # 压入栈中
    for a in bs.find_all('a')[::-1]:
        stack.push(a)

    # 查看栈中元素
    # stack.show_stack()

    while not stack.is_empty():
        # 取栈顶元素
        top_a = stack.top()
        # print(top_a[])
        # 打印h3标签的文本
        print(getHtml(url_top + top_a['href']).h3.get_text())

        # 获取栈顶元素a标签中的href属性值
        url_a1 = top_a['href']

        # 出栈
        stack.pop()

        # 跳转下一级的网页
        bs_a1 = getHtml(url_top + url_a1)

        # 判断是否还存在a标签
        if len(bs_a1.find_all('a')) != 0 :
            bs_a1 = bs_a1.find_all('a')
            # 压入栈中
            for a in bs_a1[::-1]:
                stack.push(a)

