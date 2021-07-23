from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms import SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(), Length(
                min=2, max=20)], render_kw={'style': 'width: 50ch'})
    email = StringField(
        'Email', validators=[
            DataRequired(), Email()], render_kw={
            'style': 'width: 50ch'})
    password = PasswordField(
        'Password', validators=[
            DataRequired()], render_kw={
            'style': 'width: 50ch'})
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')], render_kw={
            'style': 'width: 50ch'})
    submit = SubmitField('SignUp')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[
            DataRequired()], render_kw={
            'style': 'width: 40ch'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# option_1 = "cscareerquestions"
# option_2 = "csMajors"
# option_3 = "csinterviewproblems"
# option_4 = 'DataScienceJobs'
# option_5 = 'softwaredevelopment'
# option_6 = 'datasciencecareers'


class PostForm(FlaskForm):
    subtitle = SelectField('Select Subtopic', validators=[DataRequired()],
                           choices=[
        ('cscareerquestions', 'CS Career Questions'),
        ('csinterviewproblems', 'CS Interview Problems'),
        ('csMajors', 'CS Majors'),
        ('softwaredevelopment', 'Software Development'),
        ('datasciencecareers', 'DS Careers')
    ], render_kw={'style': 'width: 25ch'})

    username = StringField(
        'Username', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    title = StringField(
        'Title', validators=[
            DataRequired(), Length(
                min=1, max=30)])
    text = TextAreaField(
        'Post', validators=[
            DataRequired(), Length(
                max=200)], render_kw={
            'style': 'width: 50ch'})
    submit = SubmitField('Post')
