import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'keinplanheschbrudi'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bme:geheim@localhost/paitararbeit'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:geheimgeheim55@20.250.161.43/paitar2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
