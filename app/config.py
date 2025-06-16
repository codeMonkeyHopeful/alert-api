import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
    DEBUG = False
    TESTING = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    LOG_LEVEL = "WARNING"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"
