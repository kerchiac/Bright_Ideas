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
        # self.liked_by=[]
        # self.tot_likes=[]
        # self.username=[]
        self.users_liked=[]
        self.user_created=[]

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
        query = "Select * from ideas "\
                "LEFT JOIN users ON ideas.sender_id = users.id "\
                "LEFT JOIN likes on likes.idea_id=ideas.id "\
                "LEFT JOIN users as users2 on users2.id=likes.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_ideas = []
        for row in results:
            new_idea=True
            users_liked_data={
                    "id": row['users2.id'],
                    "name":row['users2.name'],
                    "alias": row['users2.alias'],
                    "email": row['users2.email'],
                    "password_un": row['users2.password_un'], #unhashed
                    "password": row['users2.password'], #hashed
                    "created_at": row['users2.created_at'],
                    "updated_at": row['users2.updated_at']
                }
            #in case of the same idea liked by different people
            if len(all_ideas)>0 and all_ideas[len(all_ideas)-1].id == row['id']:
                all_ideas[len(all_ideas)-1].users_liked.append(user.User(users_liked_data))
                new_idea=False
            
            #in case of the new idea seen at the 1st time
            if new_idea:
                idea=cls(row)
                user_created_data={
                        "id": row['users.id'],
                        "name":row['name'],
                        "alias": row['alias'],
                        "email": row['email'],
                        "password_un": row['password_un'], #unhashed
                        "password": row['password'], #hashed
                        "created_at": row['users.created_at'],
                        "updated_at": row['users.updated_at']
                }
                idea.user_created=user.User(user_created_data)
                if row['users2.id'] is not None:
                    idea.users_liked.append(user.User(users_liked_data))
                all_ideas.append(idea)
        return all_ideas

    @classmethod
    def get_this_idea(cls,data):
        query = "Select * from ideas "\
        "LEFT JOIN users ON ideas.sender_id = users.id "\
        "LEFT JOIN likes on likes.idea_id=ideas.id "\
        "LEFT JOIN users as users2 on users2.id=likes.user_id "\
        "WHERE ideas.id=%(id)s;"
        # query = "SELECT * FROM ideas "\
        #         "LEFT JOIN likes ON ideas.id = likes.idea_id "\
        #         "LEFT JOIN users ON users.id=likes.user_id "\
        #         "WHERE ideas.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        user_created_data={
            "id": results[0]['users.id'],
            "name":results[0]['name'],
            "alias": results[0]['alias'],
            "email": results[0]['email'],
            "password_un": results[0]['password_un'], #unhashed
            "password": results[0]['password'], #hashed
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at'],
            }
        idea = cls(results[0])
        # idea.user_created=user.User(user_created_data)
        idea.user_created.append(user.User(user_created_data))
        for row in results:
            users_liked_data={
                    "id": row['users2.id'],
                    "name":row['users2.name'],
                    "alias": row['users2.alias'],
                    "email": row['users2.email'],
                    "password_un": row['users2.password_un'], #unhashed
                    "password": row['users2.password'], #hashed
                    "created_at": row['users2.created_at'],
                    "updated_at": row['users2.updated_at']
                }
            idea.users_liked.append(user.User(users_liked_data))
        return idea


    @classmethod
    def like_idea(cls,data):
        query = "INSERT INTO likes (user_id,idea_id) VALUES (%(user_id)s,%(idea_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
