# run_all_spiders.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

def run_all_spiders():
    settings = get_project_settings()
    spider_loader = SpiderLoader.from_settings(settings)
    
    process = CrawlerProcess(settings)
    
    # 获取所有爬虫名称并添加到进程
    for spider_name in spider_loader.list():
        if spider_name != "weibo":
            process.crawl(spider_name)
    
    # 开始爬取
    process.start()

if __name__ == '__main__':
    run_all_spiders()