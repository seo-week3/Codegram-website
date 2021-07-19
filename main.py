from flask import Flask, render_template, url_for, flash, redirect
from flask_bcrypt import Bcrypt
import json
from Project import *
from forms import *
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'a7b24667c02b1eeecea744c063db3bd3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:codio@localhost/Codegram'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checking if entries are valid
        try:
            pw_hash = bcrypt.generate_password_hash(form.password.data.encode('utf-8'))
            user = User(username=form.username.data, email=form.email.data, password=pw_hash)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            flash(f'Your account could not be created. Due to {e}')
            return render_template('register.html', title="SignUp Page", form=form)
        else:
            flash(f'Account created for {form.username.data}')
            return render_template('home.html')
    return render_template('register.html', title="SignUp Page", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login Page', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection and nothing more
# @app.route('/')
# def testdb():
#     try:
#         db.session.query(text('1')).from_statement(text('SELECT 1')).all()
#         return '<h1>It works.</h1>'
#     except Exception as e:
#         # e holds description of the error
#         error_text = "<p>The error:<br>" + str(e) + "</p>"
#         hed = '<h1>Something is broken.</h1>'
#         return hed + error_text