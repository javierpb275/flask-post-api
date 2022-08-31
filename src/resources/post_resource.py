from models.post_model import PostModel
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

_post_parser = reqparse.RequestParser()
_post_parser.add_argument('title', type=str)
_post_parser.add_argument('description', type=str)
_post_parser.add_argument('post_image', type=str)


class MyPost(Resource):

    @jwt_required()
    def get(self, post_id):
        user_id = get_jwt_identity()
        post = PostModel.find_one(post_id=post_id, user_id=user_id)
        if not post:
            return {"error": True, "data": {"message": "Post Not Found"}}, 404
        return {"error": False,
                "data": {
                    "message": "Post Found successfully.",
                    "post": post.json()
                }}, 200

    @jwt_required(fresh=True)
    def delete(self, post_id):
        user_id = get_jwt_identity()
        post = PostModel.find_one(post_id=post_id, user_id=user_id)
        if not post:
            return {"error": True, "data": {"message": "Post Not Found"}}, 404
        post.delete_from_db()
        return {"error": False, "data": {"message": "Post Deleted Successfully"}}, 200

    @jwt_required()
    def patch(self, post_id):
        user_id = get_jwt_identity()
        post = PostModel.find_one(post_id=post_id, user_id=user_id)
        if not post:
            return {"error": True, "data": {"message": "Post Not Found"}}, 404
        data = _post_parser.parse_args()
        if data['title']:
            post.title = data['title']
        if data['description']:
            post.description = data['description']
        if data['post_image']:
            post.post_image = data['post_image']
        post.save_to_db()
        return {"error": False,
                "data": {
                    "message": "Post Updated Successfully",
                    "post": post.json()
                }}, 200


class MyPostList(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        args = request.args
        posts = [post.json() for post in PostModel.find_all(args.get("page"), args.get("per_page"), args.get('sort'), post_id=args.get("post_id"),
                                                            user_id=user_id, title=args.get("title"), description=args.get("description"))]
        return {"error": False,
                "data": {
                    "message": f"{len(posts)} Posts Found",
                    "posts": posts
                }}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if not user_id:
            return {"error": True, "data": {"message": "User Id is Required"}}, 400
        data = _post_parser.parse_args()
        if not data['title']:
            return {"error": True, "data": {"message": "Title is Required"}}, 400
        post = PostModel(user_id, **data)
        post.save_to_db()
        return {"error": False,
                "data": {
                    "message": "Post Created Successfully",
                    "post": post.json()
                }}, 201


class Post(Resource):

    @jwt_required()
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

    @jwt_required()
    def get(self):
        args = request.args
        posts = [post.json() for post in PostModel.find_all(args.get("page"), args.get("per_page"), args.get('sort'), post_id=args.get("post_id"),
                                                            user_id=args.get("user_id"), title=args.get("title"), description=args.get("description"))]
        return {"error": False,
                "data": {
                    "message": f"{len(posts)} Posts Found",
                    "posts": posts
                }}, 200
