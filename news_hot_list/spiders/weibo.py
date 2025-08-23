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
    url = "https://weibo.com/hot/mine"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, method='GET')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        wb_hot_data = response.body
        print(wb_hot_data)
