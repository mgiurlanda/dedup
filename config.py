import os
from dotenv import load_dotenv
from pathlib import Path
import urllib
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
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+DB_HOST+';PORT='+DB_PORT+';DATABASE='+DB_SCHEMA+';UID='+DB_USER+';PWD='+ DB_PASSWORD)
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False