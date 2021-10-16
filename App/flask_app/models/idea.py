from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Idea:
    db_name = 'Bright_Ideas_App'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.sender_id = db_data['sender_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id=db_data['user_id']
        self.idea_id=db_data['idea_id']

    @classmethod
    def save(cls,data):
        pass

    @classmethod
    def destroy(cls,data):
        pass
    
    @classmethod
    def get_all_ideas(cls,data):
        pass

    @classmethod
    def get_this_idea(cls,data):
        pass

    @classmethod
    def like_idea(cls,data):
        pass

    @classmethod
    def count_likes(cls,data):
        pass
