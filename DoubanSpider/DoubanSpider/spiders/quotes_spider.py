import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes" # 爬虫的名字，它是唯一的，不能重复

    def start_requests(self): # 必须返回可以继续爬下去的Requests
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): # 解析爬回来的数据，以Request作为参数
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


# yield 和 yield from 的用法
def average_gen():
    total = 0
    count = 0
    average = 0
    while True:
        new_num = yield average
        print("a")
        count += 1
        total += new_num
        average = total/count

# 委托生成器
def proxy_gen():
    while True:
        yield from average_gen()

# 调用方
calc_average = proxy_gen()
next(calc_average)            # 预激下生成器
print(calc_average.send(10))  # 打印：10.0
print(calc_average.send(20))  # 打印：15.0
print(calc_average.send(30))  # 打印：20.0

