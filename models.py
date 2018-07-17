from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'students'

    uid = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(54))
    college = db.Column(db.String(150))
    security_qn_ans = db.Column(db.String(150))
    enrollments = db.Column(db.String(1000))
    last_view= db.Column(db.String(150))
    pno = db.Column(db.String(20))


    def __init__(self, first_name, last_name, email, password, college, enrollments, last_view, securtity_qa_ans, pno):

        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)
        self.college = college
        self.enrollements = enrollments
        self.last_view = last_view
        self.securtity_qa_ans = securtity_qa_ans
        self.pno = pno

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)

