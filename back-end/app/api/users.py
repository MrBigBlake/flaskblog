import re
from flask import request, jsonify, url_for
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User

EMAIL_RE_PATTERN = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@' \
                   '((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'


@bp.route("/users", methods=["POST"])
def creat_user():
    """创建新用户"""
    data = request.get_json()
    if not data:
        return bad_request("You must post JOSN data.")

    message = {}

    # 进行字段校验
    # if not data.get("username"):
    #     message["username"] = "Please provide a valid username."
    # if not data.get("email") or not re.match(EMAIL_RE_PATTERN, data.get("email")):
    #     message["email"] = "Please provide a valid email address."
    # if not data.get("password"):
    #     message["password"] = "Please provide a valid password."
    #
    # # 用户名或邮箱是否已存在
    # if User.query.filter_by(username=data.get("username")).first():
    #     message["username"] = "Please use a different username."
    # if User.query.filter_by(username=data.get("email")).first():
    #     message["email"] = "Please use a different email address."

    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)

    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response


@bp.route("/users", methods=["GET"])
@token_auth.login_required
def get_users():
    """获取所有用户"""
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)  # 每页数量不超过100
    data = User.to_collection_dict(User.query, page, per_page, "api.get_users")
    return jsonify(data)


@bp.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
    """获取单个用户"""
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route("/users/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_user(id):
    """修改用户信息"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request("You must post Json data.")

    message = {}

    # if not data.get("username"):
    #     message["username"] = "Please provide a valid username."
    # if not data.get("email") or not re.match(EMAIL_RE_PATTERN, data.get("email")):
    #     message["email"] = "Please provide a valid email address."
    #
    # # 用户名或邮箱是否已存在
    # if User.query.filter_by(username=data.get("username")).first():
    #     message["username"] = "Please use a different username."
    # if User.query.filter_by(username=data.get("email")).first():
    #     message["email"] = "Please use a different email address."

    if message:
        return bad_request(message)

    user.from_dict(data, new_user=False)
    db.session.commit()

    return jsonify(user.to_dict())


@bp.route("/users/<int:id>", methods=["DELETE"])
@token_auth.login_required
def delete_user(id):
    pass
