from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import idea

class User:
    db = "Bright_Ideas_App"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.alias = data['alias']
        self.email = data['email']
        self.password_un = data['password_un'] #unhashed
        self.password = data['password'] #hashed
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.liked_ideas =[]
        self.ideas_posted =[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name,alias,email,password,password_un) VALUES(%(name)s,%(alias)s,%(email)s,%(password)s,%(password_un)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['name']) < 3:
            flash("Name must be at least 3 characters","register")
            is_valid= False
        if len(user['alias']) < 3:
            flash("Alias must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid

    @classmethod
    def get_by_id(cls,data):
        # query = "Select * from ideas "\
        #         "LEFT JOIN users ON ideas.sender_id = users.id "\
        #         "WHERE users.id=%(id)s;"

        query = "SELECT users.*, count(distinct ideas.id) as ideas_posted, count(distinct likes.idea_id) as liked_ideas from users "\
                "LEFT JOIN ideas on users.id=ideas.sender_id "\
                "LEFT JOIN likes on likes.user_id=users.id "\
                "WHERE users.id=%(id)s "\
                "GROUP BY users.id;"

        results = connectToMySQL(cls.db).query_db(query,data)
        user_posted = cls(results[0])
        user_posted.ideas_posted = results[0]['ideas_posted']
        user_posted.liked_ideas = results[0]['liked_ideas']
        return user_posted
