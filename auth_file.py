from werkzeug.security import safe_str_cmp
from models.user_models import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # safe_str_cmp function provides safe string comparison
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
