from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms import SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# option_1 = "cscareerquestions"
# option_2 = "csMajors"
# option_3 = "csinterviewproblems"
# option_4 = 'DataScienceJobs'
# option_5 = 'softwaredevelopment'
# option_6 = 'datasciencecareers'

class PostForm(FlaskForm):
    subtitle = SelectField('Select Subtopic',validators=[DataRequired()],
            choices=[
            ('cscareerquestions', 'CS Career Questions'),
            ('csinterviewproblems', 'CS Interview Problems'),
            ('csMajors', 'CS Majors'),
            ('softwaredevelopment', 'Software Development'),
            ('datasciencecareers', 'DS Careers')
        ])
                
    username = StringField(
        'Username', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    title = StringField(
        'Title', validators=[
            DataRequired(), Length(
                min=1, max=30)])
    text = TextAreaField('Post', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Post')
