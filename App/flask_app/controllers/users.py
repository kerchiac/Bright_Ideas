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
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "name": request.form['name'],
        "alias": request.form['alias'],
        "email": request.form['email'],
        "password_un":request.form['password'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/bright_ideas')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/bright_ideas')


@app.route('/user/<int:id>')
def get_user(id):
    data ={ 
        "id": id
    }
    return render_template('user.html',user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

