# database/models.py
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.toolify

class AITool:
    @staticmethod
    def create_indexes():
        """创建数据库索引"""
        db.tools.create_index([("name", "text")])
        db.tools.create_index([("categories", 1)])
        db.tools.create_index([("status", 1)])
    
    @staticmethod
    def insert_pending(tool_data):
        """插入待审核工具"""
        tool_data['status'] = 'pending_review'
        tool_data['created_at'] = datetime.now()
        return db.pending_tools.insert_one(tool_data).inserted_id
    
    @staticmethod
    def approve_tool(tool_id, reviewer_id, categories):
        """审核通过工具"""
        tool = db.pending_tools.find_one({"_id": tool_id})
        if tool:
            tool['status'] = 'approved'
            tool['reviewed_by'] = reviewer_id
            tool['reviewed_at'] = datetime.now()
            tool['categories'] = categories
            db.tools.insert_one(tool)
            db.pending_tools.delete_one({"_id": tool_id})
            return True
        return False