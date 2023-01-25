from .extensions import db

class BaseModel(db.Model):

    __abstract__ = True

    @classmethod
    def create (cls, **data):
        return cls(**data)
    
    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()