from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, PasswordField, DateField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Email 
      
class SharedFormSecurityFields(FlaskForm): 
    create_password = PasswordField(label='Create Password', validators=[Length(min = 8, max = 16), DataRequired(), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField(label='Confirm Password', validators=[Length(min = 8, max = 16), DataRequired()])  

class SignupForm(SharedFormSecurityFields):
    name = StringField(label='Name', validators=[DataRequired(), Length(min = 5, max = 20)]) 
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Sign up')

class UpdateProfileForm(FlaskForm): 
    name = StringField(label='Name', validators=[DataRequired(), Length(min = 5, max = 20)]) 
    email = StringField(label='Email', validators=[DataRequired(), Email()]) 
    submit = SubmitField(label='Update')

class UpdatePasswordForm(SharedFormSecurityFields): 
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Change Password")

class Login(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

 
