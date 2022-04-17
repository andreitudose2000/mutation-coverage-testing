import tempfile

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass
    SECRET_KEY = "prod"

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "dev"