from datetime import timedelta

class Config:
   SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
   SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
   PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)
   MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4MB max-limit
   BASIC_AUTH_USERNAME = 'john'
   BASIC_AUTH_PASSWORD = 'matrix'