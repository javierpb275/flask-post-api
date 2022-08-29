from config.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.Text, nullable=True)

    posts = db.relationship('PostModel', lazy='dynamic')

    def __init__(self, username, email, password, avatar):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar

    def json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'posts': [post.json() for post in self.posts.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls, page, per_page, **kwargs):
        for key, value in kwargs.copy().items():
            if not value:
                kwargs.pop(key, None)
        if not page:
            page = 1
        if not per_page:
            per_page = 10
        return cls.query.filter_by(**kwargs).paginate(int(page), int(per_page), error_out=False).items

    @classmethod
    def find_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
