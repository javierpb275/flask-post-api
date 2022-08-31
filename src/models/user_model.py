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
            'avatar': self.avatar
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def _get_sort(cls, sort):
        if not sort:
            sort = cls.user_id.desc()
        else:
            if "user_id" in sort:
                sort_by = cls.user_id
            elif "username" in sort:
                sort_by = cls.username
            elif "email" in sort:
                sort_by = cls.email
            if sort[0] == '-':
                sort = sort_by.desc()
            else:
                sort = sort_by.asc()
        return sort

    @staticmethod
    def _get_pagination(page, per_page):
        if not page:
            page = 1
        if not per_page:
            per_page = 10
        return int(page), int(per_page)

    @staticmethod
    def _remove_keys_with_empty_values(dictionary):
        for key, value in dictionary.copy().items():
            if not value:
                dictionary.pop(key, None)

    @classmethod
    def find_all(cls, page, per_page, sort, **kwargs):
        cls._remove_keys_with_empty_values(kwargs)
        page, per_page = cls._get_pagination(page, per_page)
        sort = cls._get_sort(sort)
        return cls.query.filter_by(**kwargs).order_by(sort).paginate(page, per_page, error_out=False).items

    @classmethod
    def find_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
