from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Collaboration(db.Model):
    __tablename__ = 'joint_development'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('модули.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('пользователи.id'), nullable=False)

    def __repr__(self):
        return f"<Collaboration module_id={self.module_id}, user_id={self.user_id}>"
