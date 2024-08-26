import os

class Config:
    SECRET_KEY = os.urandom(64)
    #MYSQL_HOST = os.getenv("MYSQL_HOST")
    #MYSQL_USER = os.getenv("MYSQL_USER")
    #MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    #MYSQL_DB = os.getenv("MYSQL_DB")