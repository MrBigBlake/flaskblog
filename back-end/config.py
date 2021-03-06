import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"), encoding="utf-8")  # 用来读取环境变量


class Config:
    pass
