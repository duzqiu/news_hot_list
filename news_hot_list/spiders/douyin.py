import scrapy
from urllib.parse import urlencode
from typing import Any
from scrapy.http import Response
from news_hot_list.items import NewsHotListItem
from datetime import datetime

class DouyinSpider(scrapy.Spider):
    name = "douyin"
    allowed_domains = ["douyin.com"]
    base_url = "https://so-landing.douyin.com/aweme/v1/hot/search/list/"
    params_base = {
        "aid": "581610",
        "detail_list": "1",
        "board_type": "",
        "board_sub_type": "",
        "need_board_tab": "",
        "need_covid_tab": "false",
        "version_code": "32.3.0"
    }
    params_data = [["dy_hot", "0", "", "true"],["dy_plant", "2", "seeding", "false"],
                   ["dy_entertain","2", "2", "false"],["dy_society","2", "4", "false"],
                   ["dy_sh","1", "310000", "false"]]
    # params_data = [["dy_hot", "0", "", "true"],]
    def start_requests(self):
        for params in self.params_data:
            platform = params[0]
            self.params_base["board_type"] = params[1]
            self.params_base["board_sub_type"] = params[2]
            self.params_base["need_board_tab"] = params[3]

            url = f"{self.base_url}?{urlencode(self.params_base)}"
            yield scrapy.Request(url=url, callback=self.parse, meta={"platform": platform}, method="GET")

    def parse(self, response: Response, **kwargs: Any) -> Any:
        item = NewsHotListItem()
        data = response.json()
        # trending_list = data['data']['trending_list'] #抖音实时上升榜
        word_list = data['data']['word_list']
        for word in word_list[1:]:
            item["platform"] = response.meta["platform"]
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            item['title'] = word['word']
            item['url'] = ""
            item['hot'] = word['hot_value']
            item['img'] = word['word_cover']['url_list'][0]
            yield item