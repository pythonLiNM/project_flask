from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from configXC import  config

db = SQLAlchemy()#初始化数据库，在flask很多扩展里面都可以先初始化扩展的对象，然后再去调用init_app方法去初始化

def create_app(config_name):
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])

    db.init_app(app)
    # 初始化redis存储对象
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启当前项目CSRF保护
    CSRFProtect(app)

    Session(app)
    return  app #要返回app