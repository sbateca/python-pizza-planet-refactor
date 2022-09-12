import os
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI + os.path.join(BASE_DIR, 'pizza.sqlite')
