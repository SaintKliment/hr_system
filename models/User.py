from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    full_name = db.Column(db.String(100), nullable=False)  # Полное имя (ФИО)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Почта
    password = db.Column(db.String(128), nullable=False)  # Пароль
    position = db.Column(db.String(50), nullable=True)  # Должность (опционально)

    def __repr__(self):
        return f"<User {self.full_name}, {self.position}>"
