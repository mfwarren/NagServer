import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'voapieh3pfx9qnenprq8hwenfx89awnoerf89gqxnao8w7e4gxqon3847wfyxqp'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Nag]'
    MAIL_SENDER = 'Matt Warren <matt.warren@gmail.com>'
    DEFAULT_FROM_EMAIL = 'matt.warren@gmail.com'

    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'database.sqlite'))


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'TESTdatabase.sqlite'))

config = {
    'default': DevelopmentConfig,
    'testing': TestConfig
}
