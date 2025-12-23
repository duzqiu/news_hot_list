import scrapy
from urllib.parse import urlencode
from news_hot_list.items import NewsHotListItem
from datetime import datetime
from typing import Any
from scrapy.http import Response


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    base_url = "https://top.baidu.com/board"
    params = {
        "tab": "realtime"
    }
    url = f"{base_url}?{urlencode(params)}"
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, method='GET')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        item = NewsHotListItem()
        all_data = response.xpath('//div[@class="category-wrap_iQLoo horizontal_1eKyQ"]')
        for data in all_data:
            item['platform'] = "百度"
            item['sub_title'] = "热榜"
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            item['title'] = data.xpath('.//div[@class="c-single-text-ellipsis"]/text()').get().strip()
            item['url'] = data.xpath('.//a[@class="img-wrapper_29V76"]/@href').get()
            item['img'] = data.xpath('.//a/img/@src').get()
            item['hot'] = data.xpath('.//div[@class="hot-index_1Bl1a"]/text()').get().strip()
            yield item

        
