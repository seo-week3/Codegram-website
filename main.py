from flask import Flask, render_template, url_for, flash, redirect
from flask_bcrypt import Bcrypt
import json
from Project import *
from forms import *
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from IPython.display import HTML

# username: cat
# email: cat@test.com
# password red
# git mob works

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'a7b24667c02b1eeecea744c063db3bd3'
# mysql://root:codio@localhost/Codegram
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Codegram.db'

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
    if form.validate_on_submit():  # checking if entries are valid
        try:
            pw_hash = bcrypt.generate_password_hash(
                form.password.data.encode('utf-8'))
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=pw_hash)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            flash(
                f"""Your account could not be created.
                Account already exists {e}""")
            return render_template(
                'register.html',
                title="SignUp Page",
                form=form)
        else:
            flash(f'Account created for {form.username.data}')
            return render_template('selection.html')
    return render_template('register.html', title="SignUp Page", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # check entries are right
        # user =[User(username,email,password)]
        user = User.query.filter_by(email=form.email.data).all()
        if not user:
            flash(f'User not found {form.email.data}')
            return render_template('login.html', title='Login Page', form=form)
        if not bcrypt.check_password_hash(
                user[0].password, form.password.data):
            flash(f'Incorrect password for {form.email.data}')
            return render_template('login.html', title='Login Page', form=form)
        flash(f'Logged In {form.email.data}')
        return render_template('selection.html')  # return reviews
    return render_template('login.html', title='Login Page', form=form)

# reviews html for reviews page
# Sumbit for Creating a post


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = PostForm()
    if form.validate_on_submit():  # checking if entries are valid
        user = User.query.filter_by(username=form.username.data).all()
        if not user:
            flash('Please sign up to submit a comment')
            return render_template('register.html', form=RegistrationForm())
        try:
            Update_db(
                form.subtitle.data, (str(
                    form.subtitle.data), str(
                    form.title.data), str(
                    form.text.data), str(
                    form.username.data)))
        except Exception as e:
            flash(f'Form could not be sumitted {e}')
            return render_template('selection.html')
        else:
            flash(f'Post submitted!')
            return render_template('selection.html')
    return render_template('submit.html', form=form)


@app.route('/selection', methods=['GET', 'POST'])
def selection():
    return render_template('selection.html')


@app.route('/selection_display', methods=['GET', 'POST'])
def selection_display():
    name = "datasciencecareers"
    try:
        df = loadDataset(name)
        df = df.sort_values(['user_id'], ascending=False)
    except Exception as e:
        flash(f'System is currently down, select other choice')
        return render_template('selection.html')
    else:
        x = df.to_dict('records')
        return render_template('selection_display.html', x=x)

# SELECTION ROUTES


@app.route("/cscareerquestions", methods=['GET', 'POST'])
def cscareerquestions():
    name = "cscareerquestions"
    try:
        df = loadDataset(name)
        df = df.sort_values(['user_id'], ascending=False)
    except Exception as e:
        flash(f'System is currently down, select other choice')
        return render_template('selection.html')
    else:
        x = df.to_dict('records')
        return render_template('cscareerquestions.html', x=x)


@app.route("/csMajors", methods=['GET', 'POST'])
def csMajors():
    name = "csMajors"
    try:
        df = loadDataset(name)
        df = df.sort_values(['user_id'], ascending=False)
    except Exception as e:
        flash(f'System is currently down, select other choice')
        return render_template('selection.html')
    else:
        x = df.to_dict('records')
        return render_template('csMajors.html', x=x)


@app.route("/csinterviewproblems", methods=['GET', 'POST'])
def csinterviewproblems():
    name = "csinterviewproblems"
    try:
        df = loadDataset(name)
        df = df.sort_values(['user_id'], ascending=False)
    except Exception as e:
        flash(f'System is currently down, select other choice')
        return render_template('selection.html')
    else:
        x = df.to_dict('records')  # [{author:23, 45, 45}, comment:svrevr]
        return render_template('csinterviewproblems.html', x=x)


@app.route("/DataScienceJobs", methods=['GET', 'POST'])
def DataScienceJobs():
    name = "DataScienceJobs"
    try:
        df = loadDataset(name)
    except Exception as e:
        flash(f'System is currently down, select other choice')
        return render_template('selection.html')
    else:
        df.index += 1
        df = df.drop(columns=['selftext', 'user_id'])
        df.columns = ['Author', 'Category', 'Job Description and Location']
        return render_template('DataScienceJobs.html', tables=[df.to_html(
            classes='table table-hover', justify='center', header="true")])


@app.route("/softwaredevelopment", methods=['GET', 'POST'])
def softwaredevelopment():
    name = "softwaredevelopment"
    try:
        df = loadDataset(name)
        df = df.sort_values(['user_id'], ascending=False)
    except Exception as e:
        flash(f'Server down {e}')
        return render_template('selection.html')
    else:
        x = df.to_dict('records')
        return render_template('softwaredevelopment.html', x=x)


@app.route("/datasciencecareers", methods=['GET', 'POST'])
def datasciencecareers():
    name = "datasciencecareers"
    try:
        df = loadDataset(name)
        df = df.sort_values(['user_id'], ascending=False)
    except Exception as e:
        flash(f'System is currently down, select other choice {e}')
        return render_template('selection.html')
    else:
        x = df.to_dict('records')
        return render_template('datasciencecareers.html', x=x)


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
