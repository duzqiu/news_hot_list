import json

import scrapy
from typing import Any
from datetime import datetime
from scrapy.http import Response
from urllib.parse import urlencode
from news_hot_list.items import NewsHotListItem

dict_pl = {
    "sina_hot": "热榜",
    "sina_cmnt": "热议榜",
    "sina_video": "视频热榜",
    "sina_trend": "潮流热榜",
    "sina_sport": "体育热榜",
    "sina_ent": "娱乐热榜",
    "sina_auto": "汽车热榜",
    "sina_fashion": "时尚热榜",
    "sina_travel": "旅游热榜",
    "sina_ai": "AI热榜"
}


class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.cn"]
    url_list = [
        {"hot": "https://sinanews.sina.cn/h5/top_news_list.d.html"}, # 新浪热榜
        {"other": "https://newsapp.sina.cn/api/hotlist"} # 其它热榜
    ]
    news_id_list = [
        {"sina_cmnt": "HB-1-snhs/top_news_list-hotcmnt"}, # 热议榜
        {"sina_video": "HB-1-snhs/top_news_list-minivideo"}, # 视频热榜
        {"sina_trend": "HB-1-snhs/top_news_list-trend"}, # 潮流热榜
        {"sina_sport": "HB-1-snhs/top_news_list-sport"}, # 体育热榜
        {"sina_ent": "HB-1-snhs/top_news_list-ent"}, # 娱乐热榜
        {"sina_auto": "HB-1-snhs/top_news_list-auto"}, # 汽车热榜
        {"sina_fashion": "HB-1-snhs/top_news_list-fashion"}, # 时尚热榜
        {"sina_travel": "HB-1-snhs/top_news_list-travel"}, # 旅游热榜
        {"sina_ai": "HB-1-snhs/top_news_list-ai"} # AI热榜
    ]

    def start_requests(self):
        for req_url in self.url_list:
            if req_url.keys().__contains__("hot"):
                yield scrapy.Request(url=req_url['hot'], callback=self.parse, meta={"platform": "sina_hot"}, method='GET')
            elif req_url.keys().__contains__("other"):
                params = {
                    "newsId": "",
                    "localCityCode": "",
                    "wm": "",
                    "date": ""
                }
                for news_id in self.news_id_list:
                    for key, value in news_id.items():
                        params["newsId"] = value
                        url = f"{req_url['other']}?{urlencode(params)}"
                        yield scrapy.Request(url=url, callback=self.parse, meta={"platform": key}, method='GET')
            else:
                pass

    def parse(self, response: Response, **kwargs: Any) -> Any:
        item = NewsHotListItem()
        sina_a = ['sina_hot','sina_trend', 'sina_sport','sina_ent','sina_auto','sina_fashion','sina_travel','sina_ai']
        if response.meta['platform'] in sina_a:
            if response.meta['platform'] == "sina_hot":
                all_data = response.xpath('//script/text()').getall()
                str_data = all_data[2] # 获取script中的数据 str类型
                str_data_copy = str_data[5:-1] # 截取返回字符串的json str类型
                dict_data = json.loads(str_data_copy) # 将截取的字符串json转换为json类型 json类型
                hot_list = dict_data['data']['data']['hotList'] # 获取json数据中的hot list数据
            else:
                hot_list = response.json()['data']['hotList']
            for hot in hot_list:
                item['platform'] = "新浪"
                item['icon'] = "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/08/06/0f/08060fea-34cb-2e42-fbb0-88d445d665b9/AppIcon-0-0-1x_U007emarketing-0-8-0-85-220.png/350x350.png?"
                item['sub_title'] = dict_pl[response.meta['platform']]
                item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                item['title'] = hot['base']['dynamicName']
                item['url'] = hot['base']['base']['url']
                if len(hot['base']['decoration']) == 1:
                    item['hot'] = hot['base']['decoration'][0]['hotValue']
                else:
                    item['hot'] = hot['base']['decoration'][1]['hotValue']
                item['img'] = ''
                yield item
        else:
            hot_list = response.json()['data']['hotList']
            for hot in hot_list:
                share_data = hot['info']['interactionInfo']['shareInfo']
                item['platform'] = "新浪"
                item['icon'] = "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/08/06/0f/08060fea-34cb-2e42-fbb0-88d445d665b9/AppIcon-0-0-1x_U007emarketing-0-8-0-85-220.png/350x350.png?"
                item['sub_title'] = dict_pl[response.meta['platform']]
                item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                item['title'] = share_data['customTitle']
                item['url'] = share_data['link']
                item['img'] = share_data.get('imgUrl') if share_data.get('imgUrl') else ''
                item['hot'] = ''
                yield item
