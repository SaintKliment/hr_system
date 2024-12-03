from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(255), nullable=False)
    positions = db.Column(db.JSON, nullable=False)  
    activities = db.Column(db.JSON, nullable=False)  
    data_source = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    responsible = db.Column(db.String(255), nullable=False)


def __repr__(self):
        return f"<Module {self.module_name}>"



class User(db.Model):
    __tablename__ = 'пользователи'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.fullname}>"

class Module(db.Model):
    __tablename__ = 'модули'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    positions = db.Column(db.String(255))
    data_source = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    responsible = db.Column(db.String(255), nullable=False)
    last_editor_id = db.Column(db.Integer, db.ForeignKey('пользователи.id'))

    def __repr__(self):
        return f"<Module {self.name}>"

class Collaboration(db.Model):
    __tablename__ = 'совместная_разработка'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('модули.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('пользователи.id'), nullable=False)

    def __repr__(self):
        return f"<Collaboration module_id={self.module_id}, user_id={self.user_id}>"
