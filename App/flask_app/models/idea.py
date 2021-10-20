from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math
from flask_app.models import user

class Idea:
    db_name = 'Bright_Ideas_App'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.sender_id = db_data['sender_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.liked_by=[]
        self.tot_likes=[]
        self.username=[]

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
        query = "Select * from (SELECT content, idea_id, sender_id, count(user_id) as tot_likes FROM users LEFT JOIN likes ON users.id = likes.user_id LEFT JOIN ideas ON likes.idea_id = ideas.id group by idea_id) as T1 LEFT JOIN users ON T1.sender_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        ideas = []
        for row in results:
            cls.tot_likes=row['tot_likes']
            cls.username=row['name']
            ideas.append(cls(row))
        return ideas

    @classmethod
    def get_this_idea(cls,data):
        query = "SELECT * FROM ideas LEFT JOIN likes ON ideas.id = likes.idea_id LEFT JOIN users ON users.id=likes.user_id WHERE ideas.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        idea = cls(results[0])
        for row in results:
            # # if there are no favorites
            # if row['users.id'] == None:
            #     break
            # common column names come back with specific tables attached
            data = {
                "id": row['users.id'],
                "name": row['name'],
                "alias": row['alias'],
                "email": row['email'],
                "password_un": row['password_un'], #unhashed
                "password": row['password'], #hashed
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            idea.liked_by.append(user.User(data))
        return idea


    @classmethod
    def like_idea(cls,data):
        query = "INSERT INTO likes (user_id,idea_id) VALUES (%(user_id)s,%(idea_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
