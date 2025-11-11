from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.DATABASE_URL)
        self.db = self.client['telegram_bot']
        self.users = self.db['users']
        self.logs = self.db['logs']
        
    async def add_user(self, user_id, username=None, first_name=None):
        """Add or update user in database"""
        user_data = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'joined_date': datetime.now(),
            'last_used': datetime.now(),
            'total_downloads': 0,
            'total_uploads': 0
        }
        
        existing = await self.users.find_one({'user_id': user_id})
        if existing:
            await self.users.update_one(
                {'user_id': user_id},
                {'$set': {'last_used': datetime.now()}}
            )
        else:
            await self.users.insert_one(user_data)
            
    async def update_stats(self, user_id, download=False, upload=False):
        """Update user statistics"""
        update_dict = {}
        if download:
            update_dict['$inc'] = {'total_downloads': 1}
        if upload:
            update_dict['$inc'] = {'total_uploads': 1}
            
        if update_dict:
            await self.users.update_one({'user_id': user_id}, update_dict)
            
    async def get_user(self, user_id):
        """Get user data"""
        return await self.users.find_one({'user_id': user_id})
        
    async def get_all_users(self):
        """Get all users"""
        cursor = self.users.find({})
        return await cursor.to_list(length=None)
        
    async def get_total_users(self):
        """Get total user count"""
        return await self.users.count_documents({})
        
    async def log_action(self, user_id, action, details=None):
        """Log user actions"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.now()
        }
        await self.logs.insert_one(log_data)
        
    async def get_stats(self):
        """Get overall statistics"""
        total_users = await self.get_total_users()
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_downloads': {'$sum': '$total_downloads'},
                    'total_uploads': {'$sum': '$total_uploads'}
                }
            }
        ]
        cursor = self.users.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        if result:
            return {
                'total_users': total_users,
                'total_downloads': result[0]['total_downloads'],
                'total_uploads': result[0]['total_uploads']
            }
        return {
            'total_users': total_users,
            'total_downloads': 0,
            'total_uploads': 0
        }

db = Database()
