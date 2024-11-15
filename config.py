import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-are-welcome-to-guess'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'todo-db-test-0'
