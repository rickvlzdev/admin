from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash
from project import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), nullable=False)
  create_date = db.Column(db.DateTime, default=func.now(), nullable=False)
  password_hash = db.Column(db.String(128))

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))
