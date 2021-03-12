from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

from app import models
from app.api import ping, users, tokens


def create_app(config_class=Config):
    """使用应用工厂函数来返回Flask应用"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 支持跨域
    CORS(app)

    # 初始化
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
