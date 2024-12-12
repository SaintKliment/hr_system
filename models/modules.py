from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), nullable=False) 

    def __repr__(self):
        return f'<Module {self.name}, Status: {self.status}>'
