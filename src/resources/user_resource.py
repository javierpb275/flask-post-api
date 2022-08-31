from models.user_model import UserModel
from config.blocklist import BLOCKLIST
from flask_restful import Resource, reqparse
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
import jwt

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str)
_user_parser.add_argument('email', type=str)
_user_parser.add_argument('password', type=str)
_user_parser.add_argument('avatar', type=str)


class Profile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str)

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_one(user_id=user_id)
        if not user:
            return {"error": True, "data": {"message": "User Not Found"}}, 404
        return {"error": False,
                "data": {
                    "message": "Profile obtained successfully.",
                    "user": user.json()
                }}, 200

    @jwt_required(fresh=True)
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.find_one(user_id=user_id)
        if not user:
            return {"error": True, "data": {"message": "User Not Found"}}, 404
        data = self.parser.parse_args()
        if not data['refresh_token']:
            return {"error": True, "data": {"message": "No Refresh Token was Provided"}}, 400
        user.delete_from_db()
        decoded_refresh_token = jwt.decode(data['refresh_token'], options={
                                           "verify_signature": False})
        jti_access_token = get_jwt()['jti']
        jti_refresh_token = decoded_refresh_token['jti']
        BLOCKLIST.add(jti_access_token)
        BLOCKLIST.add(jti_refresh_token)
        return {"error": False, "data": {"message": "Profile deleted successfully"}}, 200

    @jwt_required(fresh=True)
    def patch(self):
        user_id = get_jwt_identity()
        user = UserModel.find_one(user_id=user_id)
        if not user:
            return {"error": True, "data": {"message": "User Not Found"}}, 404
        data = _user_parser.parse_args()
        if data['password']:
            data['password'] = generate_password_hash(data['password'])
            user.password = data['password']
        if data['username']:
            user.username = data['username']
        if data['email']:
            user.email = data['email']
        user.save_to_db()
        return {"error": False,
                "data": {
                    "message": "Profile Updated Successfully",
                    "user": user.json()
                }}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        refresh_token = create_refresh_token(identity=current_user)
        return {"error": False,
                "data": {
                    "message": "Refreshed Token Successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }}, 200


class UserSignUp(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        if not data['email'] or not data['username'] or not data['password']:
            return {"error": True, "data": {"message": "Email, Username or Password is missing"}}, 400
        if UserModel.find_one(email=data['email']) or UserModel.find_one(username=data['username']):
            return {"error": True, "data": {"message": "Email or Username is not valid. Try Again"}}, 400
        data['password'] = generate_password_hash(data['password'])
        user = UserModel(**data)
        user.save_to_db()
        access_token = create_access_token(identity=user.user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user.user_id)
        return {"error": False,
                "data": {
                    "message": "User created successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.json()
                }}, 201


class UserSignIn(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        if not data['email'] or not data['password']:
            return {"error": True, "data": {"message": "Email or Password is missing"}}, 400
        user = UserModel.find_one(email=data['email'])
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(
                identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {"error": False,
                    "data": {
                        "message": "Logged In Successfully",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user.json()
                    }}, 200
        return {"error": True, "data": {"message": "Invalid Credentials"}}, 401


class UserSignOut(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str)

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        if not data['refresh_token']:
            return {"error": True, "data": {"message": "No Refresh Token was Provided"}}, 400
        decoded_refresh_token = jwt.decode(data['refresh_token'], options={
                                           "verify_signature": False})
        jti_access_token = get_jwt()['jti']
        jti_refresh_token = decoded_refresh_token['jti']
        BLOCKLIST.add(jti_access_token)
        BLOCKLIST.add(jti_refresh_token)
        return {"error": False, "data": {"message": "Logged Out Successfully"}}, 200


class User(Resource):

    @jwt_required()
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

    @jwt_required()
    def get(self):
        args = request.args
        users = [user.json() for user in UserModel.find_all(args.get("page"), args.get("per_page"), args.get('sort'), user_id=args.get("user_id"),
                                                            username=args.get("username"), email=args.get("email"))]
        return {"error": False,
                "data": {
                    "message": f"{len(users)} Users Found",
                    "users": users
                }}, 200
