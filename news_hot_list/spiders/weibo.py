import scrapy
from urllib.parse import urlencode
from news_hot_list.items import NewsHotListItem
from datetime import datetime
import time
from typing import Any
from scrapy.http import Response


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    base_url = "https://m.weibo.cn/api/container/getIndex"
    category = {"realtimehot": "weibo_hot", "fun": "weibo_fun", "social": "weibi_cocial"}
    # category = {"realtimehot": "weibi_cocial"}
    headers = {
        'Referer': 'https://m.weibo.cn/p/106003type=25&t=3&disable_hot=1&filter_type=realtimehot',
        'X-Requested-With': 'XMLHttpRequest'
        }

    def start_requests(self):
        for key, value in self.category.items():
            params = {
                "containerid": "106003type=25&t=3&disable_hot=1&filter_type=",
                "page_type": "08"
                }
            params['containerid'] = params['containerid'] + key
            url = f"{self.base_url}?{urlencode(params)}"
            yield scrapy.Request(
                url=url, callback=self.parse, headers = self.headers, 
                meta={"platform": value},method='GET'
                )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        print(f"响应码：{response.status}")
        item = NewsHotListItem()
        item["platform"] = response.meta["platform"]
        wb_hot_data = response.json()
        print(wb_hot_data)
        data_list = wb_hot_data['data']['cards'][0]['card_group']
        for data in data_list:
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            item['title'] = data['desc']
            item['url'] = 'https://s.weibo.com/weibo?q=' + data['desc']
            hot = data.get('desc_extr','')
            if hot:
                item['hot'] = hot if type(hot) == int else hot.split()[1]
            else:
                item['hot'] = ''
            item['img'] = data.get('pic', '')
            yield item
