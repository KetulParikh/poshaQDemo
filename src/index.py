import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

import app_config
from extension import mongo, get_log_instance

from resources.datasets import insertData, checkStatus, autoTag, autoTagStatus, downloadFile

port = os.environ.get("PORT", 5000)
log = get_log_instance(__name__)

app = Flask(__name__, root_path=os.environ.get("ROOT_PATH"))
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config["MONGO_URI"] = os.environ.get("DB_URL")

# JWT authentication config
# app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(
#     os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"))

api = Api(app)
# jwt = JWTManager(app)
# mongo.init_app(app)
CORS(app)


# @jwt.expired_token_loader
# def expired_token_callback(error):
#     return jsonify({
#         'message': 'Token has expired, please refresh your token'
#     }), 403


@app.route("/")
def index():
    log.info(os.environ.get("ROOT_PATH") + os.environ.get("ENV"))
    return "Hello from flask " + str(os.getpid())


api.add_resource(insertData, '/addData')
api.add_resource(checkStatus, '/status/<int:dataset_id>')
api.add_resource(autoTag, '/autoTag/<int:dataset_id>')
api.add_resource(autoTagStatus, '/autoTag/status/<int:dataset_id>')
api.add_resource(
    downloadFile, '/downloadFile/<int:dataset_id>/<string:format>')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=(os.environ.get("ENV") == "development"))
