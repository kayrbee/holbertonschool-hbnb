#!/usr/bin/python3

import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    DEBUG = False


class DevelopmentConfig(Config):
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
