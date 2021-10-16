from flask import render_template, session,flash,redirect,request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.idea import Idea

@app.route('/post_idea',methods=['POST'])
def post_idea():
    pass

@app.route('/destroy/idea/<int:id>')
def destroy_idea(id):
    pass

@app.route('/like/idea/<int:id>',methods=['POST'])
def like_this_idea(id):
    pass

@app.route('/like/idea')
def get_all_likes(id):
    pass

@app.route('/bright_ideas')
def all_ideas(id):
    pass
    # return render_template('dashboard.html')

@app.route('/bright_ideas/<int:id>')
def this_idea(id):
    pass
    # return render_template('this_idea.html')