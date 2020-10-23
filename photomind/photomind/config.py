from datetime import timedelta
import os

class Config:
   SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
   SQLALCHEMY_DATABASE_URI = os.environ['postgres://qexxhdcednqaso:cee7a086a79c6b4527018bdc220b1a26735a153d7c3fb8d2efc8eaaafdef0796@ec2-34-232-24-202.compute-1.amazonaws.com:5432/dc38f79c09ptv']
   PERMANENT_SESSION_LIFETIME =  timedelta(minutes=20)
   
   MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB max-limit
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
   UPLOAD_FOLDER = 'static/profile_pics'

#sqlite:///site.db