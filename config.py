from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')