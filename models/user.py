from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/
    @classmethod # 81 min 8:52
    def find_by_username(cls, username):
        # return the first username found
        return cls.query.filter_by(username=username).first()

    @classmethod # 81 min 8:52
    def find_by_id(cls, _id):
        # find the first id requested 
        return cls.query.filter_by(id=id).first()