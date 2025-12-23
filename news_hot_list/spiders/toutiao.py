import scrapy
from urllib.parse import urlencode
from news_hot_list.items import NewsHotListItem
from datetime import datetime
from typing import Any
from scrapy.http import Response


class ToutiaoSpider(scrapy.Spider):
    name = "toutiao"
    allowed_domains = ["toutiao.com"]
    base_url = "https://www.toutiao.com/hot-event/hot-board/"
    params = {
        "origin": "toutiao_pc",
        "_signature": "_02B4Z6wo00901vT9yYgAAIDCE.2en18RBNL02c0AANqVEIvz9cMx2zoZxvPsiiDsn54EeZCrLWwuGED-O85.I7udeWSbMkOxtZelfOtaXbVAdZX3UBhXMN2o4BWqZ2MjraVG4CaycB2ctUa586"
    }
    url = f"{base_url}?{urlencode(params)}"
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, method="GET")

    def parse(self, response: Response, **kwargs: Any) -> Any:
        item = NewsHotListItem()
        all_data = response.json()["data"]
        for data in all_data:
            item['platform'] = "头条"
            item['sub_title'] = "热榜"
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            item["title"] = data["Title"]
            item["hot"] = data["HotValue"]
            item["url"] = data["Url"]
            item["img"] = data["Image"]["url"]
            yield item
