from datetime import datetime, timedelta
import hashlib

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask import url_for, current_app


class PaginationAPIMixin:
    """用于分页"""

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            "items": [item.to_dict() for item in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total,
            },
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page, **kwargs),
                "next": url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                "prev": url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None,
            }

        }
        return data


class User(PaginationAPIMixin, db.Model):
    """用户"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        """User对象 -> 字典"""
        data = {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "location": self.location,
            "about_me": self.about_me,
            "member_since": self.member_since.isoformat() + "Z",
            "last_seen": self.last_seen.isoformat() + "Z",
            "_links": {
                "self": url_for("api.get_user", id=self.id),
                "avatar": self.avatar(128)
            }
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        """字典 -> User对象"""
        for field in ["username", "email"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def get_jwt(self, expires_in=600):
        now = datetime.utcnow()
        payload = {
            "user_id": self.id,
            "name": self.name if self.name else self.username,
            "exp": now + timedelta(seconds=expires_in),  # 过期时间
            "iat": now  # 签发时间
        }
        return jwt.encode(
            payload=payload,
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                jwt=token,
                key=current_app.config["SECRET_KEY"],
                algorithms="HS256"
            )
        except(jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError):
            # token过期, 或被人为修改
            return None
        return User.query.get(payload.get("user_id"))

    def avatar(self, size):
        digest = hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()
        avatar = "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)
        return avatar
