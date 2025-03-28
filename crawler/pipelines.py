# crawler/pipelines.py
import re
import hashlib
from datetime import datetime
from database.db_client import check_duplicate

class ToolifyDataPipeline:
    def process_item(self, item, spider):
        # 数据清洗
        item = self.clean_data(item)
        
        # 去重检查
        if self.is_duplicate(item):
            return None
            
        # 生成唯一ID
        item['id'] = self.generate_id(item)
        
        # 添加时间戳
        item['created_at'] = datetime.now().isoformat()
        item['updated_at'] = datetime.now().isoformat()
        
        return item
    
    def clean_data(self, item):
        """清洗数据"""
        # 清理描述中的特殊字符
        if 'description' in item:
            item['description'] = re.sub(r'[^\w\s-]', '', item['description']).strip()
        
        # 标准化URL
        if 'url' in item:
            item['url'] = item['url'].split('?')[0]  # 去除查询参数
        
        return item
    
    def is_duplicate(self, item):
        """检查是否已存在"""
        return check_duplicate(item['name'], item['official_url'])
    
    def generate_id(self, item):
        """生成唯一ID"""
        hash_str = f"{item['name']}{item['official_url']}"
        return hashlib.md5(hash_str.encode()).hexdigest()