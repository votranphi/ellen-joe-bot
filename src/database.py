import os
import asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Database:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['discord_bot_db']
        self.collection = self.db['channel_mappings']
        
        # Test connection
        try:
            self.client.admin.command('ping')
            print("✅ MongoDB Connected!")
        except Exception as e:
            print(f"❌ MongoDB Connection Failed: {e}")

    # Lấy source key (ví dụ: 'news') dựa trên Discord Channel ID hiện tại
    async def get_source_by_discord_id(self, discord_id):
        doc = await asyncio.to_thread(self.collection.find_one, {"discord_id": discord_id})
        return doc['source_key'] if doc else None

    # Lấy danh sách tất cả các kênh Discord cần forward tin từ 1 Telegram ID cụ thể
    # Dùng cho Live Listener
    async def get_discord_channels_by_tele_id(self, tele_id):
        # Vì cấu trúc lưu là 1-1 theo Discord ID, ta cần tìm tất cả doc có tele_id khớp
        cursor = self.collection.find({"tele_id": tele_id})
        docs = await asyncio.to_thread(lambda: list(cursor))
        return [doc['discord_id'] for doc in docs]

    # Lưu/Cập nhật mapping
    async def set_mapping(self, discord_id, source_key, tele_id):
        data = {
            "discord_id": discord_id,
            "source_key": source_key,
            "tele_id": tele_id
        }
        await asyncio.to_thread(
            self.collection.update_one,
            {"discord_id": discord_id}, # Tìm theo discord_id
            {"$set": data},             # Update
            upsert=True                 # Nếu chưa có thì tạo mới
        )

    async def remove_mapping(self, discord_id):
            # delete_one: Xóa dòng dữ liệu khớp với discord_id
            result = await asyncio.to_thread(self.collection.delete_one, {"discord_id": discord_id})
            # Trả về True nếu xóa thành công (tìm thấy data), False nếu không tìm thấy
            return result.deleted_count > 0

db = Database()