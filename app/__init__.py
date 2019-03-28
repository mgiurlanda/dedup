import logging
import os
import json
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy

from config import Config

import pyodbc

import dedupe

from pathlib import Path 

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    with app.app_context():
        db.init_app(app)
        db.create_all()
    # app.logger.info("App initialized")

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
 
    dedupConfigFile = Path(Config.DEDUP_CONFIG) / ''
    f = dedupConfigFile.open()
    obj = json.loads(f.read())

    for entity in obj['entities']:
            entity['query'] = "".join(entity['query'])
    
    app.config['entities'] = obj['entities']

    return app