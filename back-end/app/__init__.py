from flask import Flask
from config import Config


def create_app(config_class=Config):
    """使用应用工厂函数来返回Flask应用"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 注册蓝图
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
