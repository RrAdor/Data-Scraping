from pymongo import MongoClient
from django.conf import settings
import os

class MongoDB:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            # MongoDB connection string for localhost
            mongo_uri = "mongodb://localhost:27017/"
            self._client = MongoClient(mongo_uri)
            self._db = self._client['SentimentalScope_db']
            print("Connected to MongoDB successfully")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self._client = None
            self._db = None
    
    def get_database(self):
        """Get the database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        db = self.get_database()
        if db is not None:
            return db[collection_name]
        return None
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Singleton instance
mongodb = MongoDB()
