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
    def _get_sort(cls, sort):
        if not sort:
            sort = cls.post_id.desc()
        else:
            if "post_id" in sort:
                sort_by = cls.post_id
            elif "user_id" in sort:
                sort_by = cls.user_id
            elif "title" in sort:
                sort_by = cls.title
            elif "description" in sort:
                sort_by = cls.description
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
