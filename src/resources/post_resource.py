from models.post_model import PostModel
from flask_restful import Resource
from flask import request


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
        args = request.args
        posts = [post.json() for post in PostModel.find_all(args.get("page"), args.get("per_page"), args.get('sort'), post_id=args.get("post_id"),
                                                            user_id=args.get("user_id"), title=args.get("title"), description=args.get("description"))]
        return {"error": False,
                "data": {
                    "message": f"{len(posts)} Posts Found",
                    "posts": posts
                }}, 200
