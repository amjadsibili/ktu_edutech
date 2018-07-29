from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class SignupForm(Form) :

    first_name = StringField('Enter first name : ', validators = [DataRequired('Please enter valid first name'), Length(2,20)])
    last_name = StringField('Enter last name : ', validators = [DataRequired('Please enter valid last name'), Length(2,20)])
    email = StringField('Enter email : ', validators = [DataRequired('Please enter valid email'),Email()])
    password = PasswordField('Enter password : ', validators = [DataRequired('Please enter a new password'), EqualTo('confirm', message = 'Password mismatch'), Length(5, 20)])
    confirm = PasswordField('Confirm password : ', validators = [DataRequired('Please re-enter password'), Length(5, 20)])
    college = SelectField('Enter college : ',choices = [('mea', 'mea'),('mes', 'mes'), ('ekc', 'ekc')], validators = [DataRequired('Please enter college name, if not listed then select others')])
    security_q = SelectField('Choose a security question', choices = [('My best childhood friend was','My best childhood friend was'), ('My first school was','My first school was'), ('Where are you born','Where are you born'), ('How many siblings do you have', 'How many siblings do you have')], validators = [DataRequired()])
    security_qa = StringField('Enter answer for security question', validators = [DataRequired(), Length(2,50)])
    submit = SubmitField('Create Account')
    pno = IntegerField('Enter phone number : ', validators = [DataRequired('Please enter valid phone number')])

class LoginForm(Form) :

    email = StringField('Enter email : ', validators = [DataRequired('Please enter valid email'), Email()])
    password = PasswordField('Enter password : ', validators = [DataRequired('Please enter the password')])
    submit = SubmitField('Login')

class TestForm(Form) :

    text = StringField('enter string : ', validators = [DataRequired()])
    submit = SubmitField('Submit')

class ForgetPasswordForm(Form) :

    email = StringField('Enter registered email : ', validators = [DataRequired('Please enter the email'), Email()])
    submit = SubmitField('Submit')

class SecurityQAForm(Form) :

    answer = StringField('Enter answer', validators = [DataRequired('Please enter the answer')])
    submit = SubmitField('Next')

class ResetPasswordForm(Form) :

    password = PasswordField('Enter new password : ', validators = [DataRequired('Enter valid password'), Length(5, 20), EqualTo('confirm', message = 'Password mismatch')])
    confirm = PasswordField('Repeat new password : ', validators = [DataRequired('Enter valid password'), Length(5, 20)])
    submit = SubmitField('Reset password')

class CourseQueryForm(Form) :

    dept = SelectField('Choose department :', choices = [('cse', 'cse'), ('me', 'me'), ('ce', 'ce'), ('eee', 'eee'), ('ece', 'ece')], validators = [DataRequired('Please select a department!')])
    semester = SelectField('Select semester :', choices = [('first_year', 'first year'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], validators = [DataRequired('Please select a semester!')])
    submit = SubmitField('Find courses')
