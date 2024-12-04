from db import db

class Module(db.Model):
    __tablename__ = 'modules'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(255), nullable=False)
    positions = db.Column(db.JSON, nullable=False)  
    activities = db.Column(db.JSON, nullable=False)  
    data_source = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    responsible = db.Column(db.String(255), nullable=False)
    materials = db.Column(db.JSON, nullable=True)  


def __repr__(self):
        return f"<Module {self.module_name}>"
