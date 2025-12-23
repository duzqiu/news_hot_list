# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsHotListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform = scrapy.Field() # 平台
    title = scrapy.Field() # 标题
    sub_title = scrapy.Field() # 副标题
    url = scrapy.Field() # 链接
    img = scrapy.Field() # 缩略图地址
    hot = scrapy.Field() # 热度
    create_time = scrapy.Field() # 创建时间
    pass
