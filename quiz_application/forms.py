from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

from quiz_application.models import Subject 
      
class SharedFormSecurityFields(FlaskForm): 
    create_password = PasswordField(label='Create Password', validators=[Length(min = 8, max = 16), DataRequired(), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField(label='Confirm Password', validators=[Length(min = 8, max = 16), DataRequired()])  

class SignupForm(SharedFormSecurityFields):
    name = StringField(label='Name', validators=[DataRequired(), Length(min = 5, max = 20)]) 
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(max = 20)])
    submit = SubmitField(label='Sign up')

class UpdateProfileForm(FlaskForm): 
    name = StringField(label='Name', validators=[DataRequired(), Length(min = 5, max = 20)]) 
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(max = 20)]) 
    submit = SubmitField(label='Update')

class UpdatePasswordForm(SharedFormSecurityFields): 
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Change Password")

class Login(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class SubjectForm(FlaskForm):
    subject_name = StringField(label="Subject", validators=[DataRequired(), Length(min = 2, max = 20)])
    subject_about = StringField(label="About", validators=[DataRequired(), Length(min = 5, max = 40)])
    submit = SubmitField(label="Create")

class QuestionForm(FlaskForm):
    question = StringField(label="Question", validators=[DataRequired(), Length(min = 5, max = 45)])
    choice_one = StringField(label="Choice One",  validators=[DataRequired(), Length(min = 3, max = 25)])
    choice_two = StringField(label="Choice Two",  validators=[DataRequired(), Length(min = 3, max = 25)])
    choice_three = StringField(label="Choice Three",  validators=[DataRequired(), Length(min = 3, max = 25)])
    correct_answer = StringField(label="Correct Answer",  validators=[DataRequired(), Length(min = 3, max = 25)])
    subjects = SelectField(label="Subejct", validators=[DataRequired()], choices=[])
    submit = SubmitField(label="Create Question")  
    
class UpdateUserForm(FlaskForm): 
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(max = 20)]) 
    name = StringField(label='Name', validators=[DataRequired(), Length(min = 5, max = 20)])  
    role = SelectField(label="Role", validators=[DataRequired()], choices=[])  
    submit = SubmitField(label="Update User")  