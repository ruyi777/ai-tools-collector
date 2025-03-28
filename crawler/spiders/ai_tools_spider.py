# crawler/spiders/ai_tools_spider.py
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
import json
from datetime import datetime

class ProductHuntAISpider(scrapy.Spider):
    name = "producthunt_ai"
    allowed_domains = ["www.producthunt.com"]
    start_urls = ["https://www.producthunt.com/topics/ai"]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; ToolifyAIBot/1.0; +https://toolify.ai/bot)',
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1
    }

    def parse(self, response):
        # 解析Product Hunt的AI工具列表
        tools = response.css('div[data-test="post-item"]')
        
        for tool in tools:
            item = {
                'source': 'ProductHunt',
                'scraped_at': datetime.now().isoformat(),
                'status': 'pending_review'
            }
            
            # 基础信息提取
            item['name'] = tool.css('h3::text').get().strip()
            item['url'] = f"https://www.producthunt.com{tool.css('a::attr(href)').get()}"
            item['description'] = tool.css('p[class*="postItem_tagline"]::text').get().strip()
            item['votes'] = int(tool.css('div[class*="voteButtonContainer"] span::text').get())
            
            # 获取标签分类
            item['categories'] = tool.css('div[class*="topics"] a::text').getall()
            
            # 进入详情页获取更多信息
            yield response.follow(
                item['url'],
                callback=self.parse_tool_detail,
                meta={'item': item}
            )

    def parse_tool_detail(self, response):
        item = response.meta['item']
        
        # 提取详情页信息
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取网站链接
        launch_link = soup.find('a', {'data-test': 'launch-link'})
        if launch_link:
            item['official_url'] = launch_link['href']
        
        # 获取截图
        item['screenshots'] = []
        for img in soup.select('div.gallery img'):
            if img.get('src'):
                item['screenshots'].append(img['src'])
        
        # 获取定价信息
        pricing_div = soup.find('div', string='Pricing')
        if pricing_div:
            item['pricing'] = pricing_div.find_next_sibling('div').get_text(strip=True)
        
        yield item


class GitHubAISpider(scrapy.Spider):
    name = "github_ai"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/topics/artificial-intelligence"]
    
    # 类似实现...