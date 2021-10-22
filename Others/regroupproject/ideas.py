from flask import render_template, session,flash,redirect,request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.idea import Idea

@app.route('/post_idea',methods=['POST'])
def post_idea():
    if 'user_id' not in session:  #check if user login
        return redirect('/')
    data = {
        "content":  request.form['content'],
        "sender_id": session['user_id']
    }
    Idea.save(data)
    return redirect('/bright_ideas')

@app.route('/destroy/idea/<int:id>')
def destroy_idea(id):
    data = {
        "id": id
    }
    Idea.destroy(data)
    return redirect('/bright_ideas')

@app.route('/like/idea/<int:id>',methods=['POST'])
def like_this_idea(id):
    data = {
        "idea_id": id,
        "user_id": 'user_id'
    }
    Idea.like_idea(data)
    return redirect('/bright_ideas')

@app.route('/bright_ideas')
def all_ideas():
    data ={
        'id': session['user_id']
    }
    return render_template('dashboard.html',ideas=Idea.get_all_ideas(),user=User.get_by_id(data))


@app.route('/bright_ideas/<int:id>')
def this_idea(id):
    data={
        "id": id,
    }
    data2={
        'id': session['user_id']
    }
    return render_template('this_idea.html',idea=Idea.get_this_idea(data),user=User.get_by_id(data2))