import scrapy
from urllib.parse import urlencode
from typing import Any
from scrapy.http import Response
from news_hot_list.items import NewsHotListItem
from datetime import datetime

class BilibiliSpider(scrapy.Spider):
    name = "bilibili"
    allowed_domains = ["bilibili.com"]
    url = "https://app.bilibili.com/x/v2/search/trending/ranking?limit=30"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, method='GET')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        item = NewsHotListItem()
        data_list = response.json()['data']['list']
        top_data = response.json()['data']['top_list']
        item['platform'] = 'bilibili'
        item['title'] = top_data[0]['show_name']
        item['url'] = ''
        item['img'] = ''
        item['hot'] = ''
        item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        yield item
        for data in data_list:
            item['platform'] = 'bilibili'
            item['title'] = data['show_name']
            item['url'] = ''
            item['img'] = ''
            item['hot'] = ''
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            yield item


