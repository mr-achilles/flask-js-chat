import os


class Config(object):
    SECRET_KEY = b'n\x8e\t\x16\xa2\x86k\xaeF\x0e\xcb\xd385!$'
    WTF_CSRF_SECRET_KEY = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
    # database config
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/chat_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
