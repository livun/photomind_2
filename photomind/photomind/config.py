from datetime import timedelta


class Config:
   SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
   SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
   PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)
   
   MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB max-limit
   
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

   UPLOAD_FOLDER = 'static/profile_pics'
 
   