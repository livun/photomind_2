import os


class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SECRET_KEY='5791628bb0b13ce0c676dfde280ba245'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
    EMAIL_USER='photomind2020@gmail.com'
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    EMAIL_PASS='flask_app_project'
