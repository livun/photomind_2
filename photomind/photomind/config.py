from datetime import timedelta
import os


class Config:
   SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
   SQLALCHEMY_DATABASE_URI = 'postgres://qwjhghlshuwupj:75f24c064a2117dc42181e708496215379e7860f00524444e3d46846667b89f8@ec2-23-20-70-32.compute-1.amazonaws.com:5432/d9e3nhk9khk09m'
   PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)
   
   MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB max-limit
   
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

   UPLOAD_FOLDER = 'static/profile_pics'
