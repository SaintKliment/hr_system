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
