import os
from flask_pymongo import PyMongo
from functools import wraps
from flask import request

from logger import logger

mongo = PyMongo()

# Log file extension

root_dir = os.environ.get("ROOT_PATH")
log_dir = os.path.join(root_dir, os.environ.get("LOG_PATH"))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file_name = os.path.join(log_dir, os.environ.get("LOG_FILE_NAME"))


def get_log_instance(file_name):
    if os.environ.get("ENV") == "development":
        log = logger.get_root_logger(file_name)
    else:
        log = logger.get_root_logger(file_name, file_name=log_file_name)
    return log

# Basic authentication


def basic_auth(f):
    ''' This decorater chesck for auth header '''
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.headers.get("auth")
        if auth == os.environ.get("auth_token"):
            return f(*args, **kwargs)
        else:
            return {"message": "Authorization required!!!"}, 401
    return decorator

# Conditional authentication


def conditional_auth(dec, env):
    ''' If app is running on development/ test env then no authentication required '''
    def decorator(func):
        if env in ["development", "test"]:
            # Return the function unchanged, not decorated.
            return func
        return dec(func)

    return decorator
