import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from configXC import  config


db = SQLAlchemy()#初始化数据库，在flask很多扩展里面都可以先初始化扩展的对象，然后再去调用init_app方法去初始化

redis_store = None # type: StrictRedis
# redis_store:StrictRedis = None

def setup_log(config_name):
    #设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    #创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log',maxBytes=1024*1024*100,backupCount=10)
    #创建日志记录格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    #为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    #为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
def create_app(config_name):
    #配置日志,并且传入配置名字，以便能货渠道制定配置所对应的日志等级
    setup_log(config_name)
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])

    db.init_app(app)
    global redis_store
    # 初始化redis存储对象
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启当前项目CSRF保护
    CSRFProtect(app)
    Session(app)
    from info.modules.index import index_blu
    #注册蓝图
    app.register_blueprint(index_blu)


    return  app #要返回app
