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
        item['platform'] = '哔哩哔哩'
        item['sub_title'] = '热搜'
        item['icon'] = 'https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/74/c2/f5/74c2f550-18c1-4594-9f2a-1a7478416178/AppIcon-0-0-1x_U007epad-0-1-0-85-220.png/350x350.png?'
        item['title'] = top_data[0]['show_name']
        item['url'] = ''
        item['img'] = ''
        item['hot'] = ''
        item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        yield item
        for data in data_list:
            item['platform'] = '哔哩哔哩'
            item['sub_title'] = '热搜'
            item['icon'] = 'https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/74/c2/f5/74c2f550-18c1-4594-9f2a-1a7478416178/AppIcon-0-0-1x_U007epad-0-1-0-85-220.png/350x350.png?'
            item['title'] = data['show_name']
            item['url'] = ''
            item['img'] = ''
            item['hot'] = ''
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            yield item


