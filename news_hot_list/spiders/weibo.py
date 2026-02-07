import scrapy
from urllib.parse import urlencode
from news_hot_list.items import NewsHotListItem
from datetime import datetime
import time
from typing import Any
from scrapy.http import Response


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]
    cookies = {"XSRF-TOKEN": "-HBfo8UuIJi3S4aL4wRmiqLI",
               "SUB": "_2AkMe2liQf8NxqwFRmvETzmPkaoh2zwjEieKohqlLJRMxHRl-yT8XqkcotRB6NVp2f6IsBuaKNYvOaqDqDqgzM1CHSmsM", 
               "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWC0jyap89oZYk3CkWXhWXc",
               "WBPSESS": "3CRDTjRX3vAz9JRDHxBb5ANtlhC1vouM4ub2Q4ZnDerq9tbcr2J7kcUiWaRZFtoRNvKJeUIsUPkES6OIa4ft_Na7YpA7plAfhQuif5JJavmKCk1WZyODUT5O2CKW1tdP"
    }
    # https://weibo.com/ajax/statuses/mineBand
    # https://weibo.com/ajax/side/hotSearch
    # https://weibo.com/ajax/statuses/entertainment
    # https://weibo.com/ajax/statuses/life
    # https://weibo.com/ajax/statuses/social
    url = "https://weibo.com/hot/mine" # mine-我的，search-热搜，entertainment-文娱，life-生活，social-社会
    # url = "https://weibo.com/ajax/statuses/mineBand"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, cookies=self.cookies, method='GET')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        wb_hot_data = response.body
        print(wb_hot_data)
