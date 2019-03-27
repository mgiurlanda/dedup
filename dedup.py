from app import create_app
from config import Config
import click
from flask import Flask
from flask.cli import with_appcontext
from app.cleansing.dedupers import run

app = create_app()

@app.cli.command("dedup")
@click.option('--entity')
@click.argument('entity')
def dedup(entity):
    run(app.config, entity)

app.cli.add_command(dedup)