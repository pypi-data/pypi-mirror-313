import os
from pymongo import MongoClient
from dotenv import load_dotenv

class DBClient:
    def __init__(self, mongo_uri):
        """初始化時接收 MongoDB 連接 URI"""
        self.client = MongoClient(mongo_uri)
        self.db = self.client["twse_company"]
    
    def get_client(self):
        return self.client

    def get_collection(self, collection_name):
        """返回指定名稱的集合"""
        return self.db[collection_name]