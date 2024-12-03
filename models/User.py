from db import db

# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)  
    position = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<User {self.full_name}>'
