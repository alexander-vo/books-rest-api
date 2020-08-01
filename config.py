class Config:
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'development'
    TESTING = True
