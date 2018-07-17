from flask import Flask, render_template, url_for, redirect, request, flash, session
from forms import SignupForm, LoginForm
from models import User, db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<password>@localhost:5432/test'
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

    return render_template('dashboard.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signup() :

    if 'email' in session :
        return redirect(url_for('dashboard'))
    form = SignupForm()

    if request.method == 'POST' :
        if form.validate() == False :
            return render_template('signup.html', form = form)
        else :
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.college.data, 'Nil', 'Nil', form.security_qa.data, form.pno.data)
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

    elif request.method == 'GET' :
        return render_template('login.html', form = form)


@app.route('/logout')
def logout() :

    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':

    app.run(debug = True)
