from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math


class Idea:
    db_name = 'Bright_Ideas_App'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        # self.sender_id = db_data['sender_id']
        # self.created_at = db_data['created_at']
        # self.updated_at = db_data['updated_at']
        # self.user_id=db_data['user_id']
        self.user_name=db_data['name']
        # self.user_alias=db_data['alias']
        # self.idea_id=db_data['idea_id']
        # self.tot_likes=db_data['tot_likes']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO ideas (content,sender_id) VALUES (%(content)s,%(sender_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM ideas WHERE ideas.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all_ideas(cls):
        query = "Select idea_id as id, content,users.name as name, tot_likes from (SELECT content, idea_id, sender_id, count(user_id) as tot_likes FROM users LEFT JOIN likes ON users.id = likes.user_id LEFT JOIN ideas ON likes.idea_id = ideas.id group by idea_id) as T1 LEFT JOIN users ON T1.sender_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        ideas = []
        for row in results:
            ideas.append( cls(row))
        return ideas

    @classmethod
    def get_this_idea(cls,data):
        query = "SELECT likes.id as id, email as content, name, alias, user_id FROM users LEFT JOIN likes ON users.id = likes.user_id where idea_id=15"
        results = connectToMySQL(cls.db_name).query_db(query)
        users_liked = []
        for row in results:
            users_liked.append( cls(row))
        return users_liked

    @classmethod
    def like_idea(cls,data):
        query = "INSERT INTO likes (user_id,idea_id) VALUES (%(user_id)s,%(idea_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
