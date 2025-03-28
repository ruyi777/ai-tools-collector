# crawler/run_crawlers.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.ai_tools_spider import ProductHuntAISpider, GitHubAISpider, AITopicsSpider
import schedule
import time
from database.db_client import save_to_pending

def run_spiders():
    process = CrawlerProcess(get_project_settings())
    
    # 注册所有爬虫
    process.crawl(ProductHuntAISpider)
    process.crawl(GitHubAISpider)
    process.crawl(AITopicsSpider)
    
    # 启动爬虫
    process.start()
    
    # 将结果存入待审核数据库
    for spider in process.spiders:
        save_to_pending(spider.collected_items)

# 定时任务
schedule.every(6).hours.do(run_spiders)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)