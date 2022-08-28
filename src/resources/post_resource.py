from models.post_model import PostModel
from flask_restful import Resource


class Post(Resource):

    def get(self, post_id):
        post = PostModel.find_one(post_id=post_id)
        if not post:
            return {"error": True, "data": {"message": "Post Not Found"}}, 404
        return {"error": False,
                "data": {
                    "message": "Post Found successfully.",
                    "post": post.json()
                }}, 200


class PostList(Resource):

    def get(self):
        posts = [post.json() for post in PostModel.find_all()]
        return {"error": False,
                "data": {
                    "message": f"{len(posts)} Posts Found",
                    "posts": posts
                }}, 200