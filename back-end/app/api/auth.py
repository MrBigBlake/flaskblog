from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """用于校验用户名和密码"""
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user = user
    return user.check_password(password)


@token_auth.verify_token
def verify_token(token):
    """用于校验请求是否携带有效的token"""
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@basic_auth.error_handler
def basic_auth_error():
    """用于在认证失败的情况下返回错误响应"""
    return error_response(401)


@token_auth.error_handler
def token_error():
    """用于在token认证失败的情况下返回错误响应"""
    return error_response(401)
