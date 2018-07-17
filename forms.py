from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo

class SignupForm(Form) :

    first_name = StringField('Enter first name : ', validators = [DataRequired()])
    last_name = StringField('Enter last name : ', validators = [DataRequired()])
    email = StringField('Enter email : ', validators = [DataRequired()])
    password = PasswordField('Enter password : ', validators = [DataRequired()])
    confirm = PasswordField('Confirm password : ', validators = [DataRequired(), EqualTo('confirm', message = 'Password mismatch')])
    college = StringField('Enter college : ', validators = [DataRequired()])
    security_qa = StringField('Enter security answer : ', validators = [DataRequired()])
    submit = SubmitField('Create Account')
    pno = IntegerField('Enter phone number : ', validators = [DataRequired()])

class LoginForm(Form) :

    email = StringField('Enter email : ', validators = [DataRequired()])
    password = PasswordField('Enter password : ', validators = [DataRequired()])
    submit = SubmitField('Login')