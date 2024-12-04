from db import db

class Collaboration(db.Model):
    __tablename__ = 'joint_development'  
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

    def __repr__(self):
        return f"<Collaboration module_id={self.module_id}, user_id={self.user_id}>"