# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import random

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo

class MongoDBPipeline:
    def __init__(self, mongo_url, mongo_db, collection_name):
        self.client = None
        self.db = None
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.collection = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'news_hot_list'),
            collection_name=crawler.settings.get('MONGO_COLLECTION', 'news_hot')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection]

    def close_spider(self, spider):
        # self.collection.close()
        # self.db.close()
        self.client.close()

    def process_item(self, item, spider):
        try:
            # 将 Item 转换为字典并插入到 MongoDB
            self.collection.insert_one(dict(item))
            spider.logger.info(f"Item inserted into MongoDB: {item}")
        except Exception as e:
            spider.logger.error(f"Error inserting item into MongoDB: {e}")
            raise DropItem(f"Error inserting item into MongoDB: {e}")
        
        return item


class NewsHotListPipeline:
    def process_item(self, item, spider):
        if item['img']:
            pass
        else:
            item['img'] = "https://www.logo9.net/userfiles/images/9JINRTT1.jpg"
        if item['hot']:
            if str(item['hot']).endswith("万"):
                pass
            else:
                num = int(item['hot'])
                if num >= 10000:
                    num_in_wan = num // 10000  # 使用整除，直接得到整数部分
                    result = f"{num_in_wan}万"
                    item['hot'] = result
                else:
                    pass
        else:
            num = random.randint(100, 900)
            item['hot'] = f"{num}万"
        return item
