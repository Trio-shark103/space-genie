from Sates import db, login_manager
from Sates import bcrypt
from flask_login import UserMixin

#adding a login loader call back to help flask recall the login_page
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column (db.String(length=30), nullable=False, unique=True)
    email_address= db.Column (db.String(length=50),nullable=False,unique=True)
    password_hash = db.Column(db.Integer(),nullable=False)
    
    # hashing of passwords of users
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    # for attempted user with wrong password
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
            

class Satellite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    continent = db.Column(db.String(50), nullable=False)
    satellite_type = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)

def __repr__(self):
    return f'User {self.name}'