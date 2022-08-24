from config.db import db
from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config.blocklist import BLOCKLIST

app = Flask(__name__)

load_dotenv('config/.env')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

db.init_app(app)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_data):
    return jwt_data['jti'] in BLOCKLIST

api = Api(app)

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello world!!"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)