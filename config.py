import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A_|g7o1{cly>>YI'
