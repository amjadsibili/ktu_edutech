#TODO forget password- signup
#TODO next: dashboard
#TODO phone no limit = 10 with js front end
#TODO check csrf exploitablilty (id generated in sc)
#TODO one way hash algorithm for sessions storage
#TODO login back re-routing 404 error - DONE
#TODO exception when non existant email entered - forget password
#Error 404 -> maybe cuz GET request not defined
#TODO catch 500, 404 exceptions and redirect/render
#TODO incorrect pass/user - login message
#TODO Dashboard - print all enrolled courses

from flask import Flask, render_template, url_for, redirect, request, flash, session
from forms import SignupForm, LoginForm, SecurityQAForm, ForgetPasswordForm, ResetPasswordForm, CourseQueryForm
from models import User, db
from db_parsers import UserEntity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mamm0th@localhost:5432/test'
app.secret_key = 'development-key'
db.init_app(app)

@app.route('/')
def index() :

    return redirect(url_for('home'))

@app.route('/home')
def home() :
    flash('welcome', 'error')
    return render_template('home.html')



@app.route('/dashboard')
def dashboard() :

    if 'email' not in session :
        return redirect(url_for('home'))
    if request.method == 'GET' :
        query = "SELECT * FROM students WHERE email="+"'"+session['email']+"';"
        user = ''
        for i in db.engine.execute(query) :
            user = i
        user_cred = {'fname' : user[1], 'enrollments' : user[6], 'last_viewed' : user[7]}
        new_user = False
        if user_cred['enrollments'] == 'Nil' :
            new_user = True
        return render_template('dashboard.html', user_cred = user_cred, new_user = new_user)



@app.route('/signup', methods = ['GET', 'POST'])
def signup() :

    def make_sec_qa_dict(security_q, security_qa) :
        if security_q == 'My best childhood friend was' :
            dic = {1: security_qa}
        elif security_q == 'My first school was' :
            dic = {2: security_qa}
        elif security_q == 'Where are you born' :
            dic = {3: security_qa}
        elif security_q == 'How many siblings do you have' :
            dic = {4: security_qa}
        return str(dic)

    def email_check(mail) :
        query = 'SELECT email FROM students;'
        res = db.engine.execute(query)
        exists = False
        for row in res :
            if row[0] == mail :
                exists = True
        return exists


    if 'email' in session :
        return redirect(url_for('dashboard'))
    form = SignupForm()

    if request.method == 'POST' :
        if form.validate() == False :
            return render_template('signup.html', form = form)
        if email_check(form.email.data) == True :
            return render_template('signup.html', form = form, message = 'Email already exists.')
        else :

            sec_qa_dict = make_sec_qa_dict(form.security_q.data, form.security_qa.data)
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.college.data, 'Nil', 'Nil', sec_qa_dict, form.pno.data)
            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            return redirect(url_for('dashboard'))
    #
    elif request.method == 'GET' :
        return render_template('signup.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login() :

    if 'email' in session :
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == 'POST' :
        if form.validate() == False :
            return render_template('login.html', form = form)
        else :
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email = email).first()

            if user is not None and user.check_password(password) :
                session['email'] = form.email.data
                return redirect(url_for('dashboard'))
            else :
                return redirect(url_for('login'))


    return render_template('login.html', form = form)


@app.route('/login/forgot_password', methods = ['GET', 'POST'])
def forgot_password() :


    if 'email' in session :
        return redirect(url_for('dashboard'))

    form = ForgetPasswordForm()
    if request.method == 'GET' :
        return render_template('forgot_password.html', form = form)
    elif request.method == 'POST' :

        email = form.email.data
        query = "SELECT email FROM students WHERE email="+"'"+email+"';"
        results = db.engine.execute(query)
        email_exists = False

        for tup in results :
            if tup[0] == email :
                email_exists = True

        if email_exists :
            session['email_exists'] = email
            query = "SELECT security_qn_ans FROM students WHERE email="+"'"+email+"';"
            res = db.engine.execute(query)
            for row in res :
                temp = row
            qn, ans = UserEntity.SecurityQAParser((temp[0]))
            session['qn'] = qn
            return redirect(url_for('confirm'))
        else :
            return render_template('forgot_password.html', message = 'Email not registered.', form = form)


@app.route('/logout')
def logout() :

    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/login/forgot_password/confirm', methods = ['GET', 'POST'])
def confirm() :


    if 'email_exists' not in session :
        return redirect(url_for('home'))
    else :
        form = SecurityQAForm()
        qn = ''
        ans = ''
        if request.method == 'GET' :
            return render_template('confirm.html', form = form, qn = session['qn'])
            session.pop('qn', None)
        elif request.method == 'POST' :
            query = "SELECT security_qn_ans FROM students WHERE email="+"'"+session['email_exists']+"';"
            res = db.engine.execute(query)
            for row in res :
                temp = row
            qn, ans = UserEntity.SecurityQAParser(temp[0])
            if ans.lower() == form.answer.data.lower() :
                return render_template('reset.html', form = ResetPasswordForm())
            else :
                return render_template('confirm.html', form = form, message = 'Answer does not match!')
    return 'confirm'

@app.route('/reset', methods = ['GET', 'POST'])
def reset() :

    if 'email_exists' not in session :
        return redirect(url_for('home'))
    else :

        email = session['email_exists']
        form = ResetPasswordForm()
        if request.method == 'POST' : #Not coming to this block!
            if form.validate() == False :
                return render_template('reset.html', form = form)
            else :

                new_pass = form.password.data
                from werkzeug import generate_password_hash
                hash_pass = generate_password_hash(new_pass)
                query = "UPDATE students SET password_hash="+"'"+hash_pass+"'"+"WHERE email="+"'"+session['email_exists']+"';"
                db.engine.execute(query)
                session.pop('email_exists', None)
                #print (session['email_exists'])
                return redirect(url_for('login'))

        elif request.method == 'GET' :
            return render_template('reset.html', form = form)

@app.route('/courses', methods = ['GET', 'POST'])
def courses() :

    enrollable = False

    if 'email' not in session :
        enrollable = True

    form = CourseQueryForm()
    if request.method == 'GET' :
        return render_template('courses.html', form = form)
    elif request.method == 'POST' :
        dept = form.dept.data
        semester = form.semester.data
        query = "SELECT duration, cname FROM courses WHERE branch="+"'"+dept+"'"+"AND semester="+"'"+semester+"';"
        results = db.engine.execute(query)
    


@app.errorhandler(404)
def page_not_found(e) :
    return redirect(url_for('home'))

@app.errorhandler(500)
def page_not_found(e) :
    return render_template('sorry.html')

@app.route('/test', methods = ['GET', 'POST'])
def test() :
    pass
