import os
from dotenv import load_dotenv
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(Path(basedir) / '.env')

class Config:
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_SCHEMA = os.environ.get('DB_SCHEMA') or 'Alex'
    DB_USER = os.environ.get('DB_USER') or 'alex'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'alex'
    DB_PORT = os.environ.get('DB_PORT') or '1443'
    DEDUPE_SETTINGS = os.environ.get('DEDUPE_SETTINGS') or 'dedupe_settings'
    DEDUPE_TRAINING = os.environ.get('DEDUPE_TRAINING') or 'training.json'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or True
    DEDUP_CONFIG = os.environ.get('DEDUP_CONF')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False