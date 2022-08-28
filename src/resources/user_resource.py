from models.user_model import UserModel
from flask_restful import Resource


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_one(user_id=user_id)
        if not user:
            return {"error": True, "data": {"message": "User Not Found"}}, 404
        return {"error": False,
                "data": {
                    "message": "User Found successfully.",
                    "user": user.json()
                }}, 200


class UserList(Resource):

    def get(self):
        users = [user.json() for user in UserModel.find_all()]
        return {"error": False,
                "data": {
                    "message": f"{len(users)} Users Found",
                    "users": users
                }}, 200
