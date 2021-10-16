from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.idea import Idea
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register',methods=['POST'])
def register():
    pass

@app.route('/login',methods=['POST'])
def login():
    pass

@app.route('/user/<int:id>')
def user():
    pass
    # return render_template('user.html')

@app.route('/logout')
def logout():
    pass

