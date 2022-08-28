from config.db import db


class PostModel(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=True)
    post_image = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id, title, description, post_image):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.post_image = post_image

    def json(self):
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "post_image": self.post_image,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls, **kwargs):
        if not kwargs:
            return cls.query.all()
        return cls.query.filter_by(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
