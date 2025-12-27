from dotenv import load_dotenv

load_dotenv()

import os 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-new')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///gearguard.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False