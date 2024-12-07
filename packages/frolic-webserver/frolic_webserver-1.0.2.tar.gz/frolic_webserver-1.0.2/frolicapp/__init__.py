import sys
import tomllib
from typing import Any, NoReturn
import click
from flask import Flask, redirect, render_template, url_for, send_from_directory
from jinja2 import TemplateError
from werkzeug import Response, exceptions
from flask.cli import FlaskGroup
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from flask_sqlalchemy import SQLAlchemy
import os
from enum import StrEnum, auto


title = '''


    ███████╗██████╗  ██████╗ ██╗     ██╗ ██████╗     ██████╗██╗     ██╗
    ██╔════╝██╔══██╗██╔═══██╗██║     ██║██╔════╝    ██╔════╝██║     ██║
    █████╗  ██████╔╝██║   ██║██║     ██║██║         ██║     ██║     ██║
    ██╔══╝  ██╔══██╗██║   ██║██║     ██║██║         ██║     ██║     ██║
    ██║     ██║  ██║╚██████╔╝███████╗██║╚██████╗    ╚██████╗███████╗██║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═════╝╚══════╝╚═╝
                                                                       

''' 


class Base(MappedAsDataclass, DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)
assets_dir = os.path.join('assets')
profile_pictures_dir = os.path.join(assets_dir, 'profile_pictures')
thumbnails_dir = os.path.join(assets_dir, 'thumbnails')

def ensure_configuration_availability(instance_path: str) -> str:
    """Ensure the availability of configuration file optionally set fron environment variable PROFILE at given path."""
    if not os.path.exists(instance_path):
        try:
            os.makedirs(instance_path)
        except Exception as e:
            click.echo(click.style(f"Cannot create instance directory.\n{str(e)}", fg='red', bold=True))
            sys.exit()
    profile = os.getenv('PROFILE', 'Deployment')
    abs_config_path = os.path.join(instance_path, profile+'.toml')
    if not os.path.exists(abs_config_path):
        with open(abs_config_path, 'w'):
            pass
        click.echo(click.style(f"An empty configuration file has been generated for this application at {abs_config_path} .", fg='bright_blue', bold=True))
    return profile+'.toml'


def make_app() -> Flask:
    application = Flask(__name__, instance_relative_config=True)
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    application.config['SQLALCHEMY_ECHO'] = True
    application.config['SECRET_KEY'] = '3a5bda5b2089cfc46eb2beec26d25f6e5c63f35c53af7b136ca270a66c6f9653'

    config_file = ensure_configuration_availability(application.instance_path)
    application.config.from_file(config_file, load=tomllib.load, text=False)

    import frolicapp.cli as cli
    application.cli.add_command(cli.test)
    application.cli.add_command(cli.create)
    application.cli.add_command(cli.clean)
    application.cli.add_command(cli.mock)

    db.init_app(application)

    from .blueprints import admin
    application.register_blueprint(admin.bp)

    @application.get('/')
    def home() -> Response:
        return redirect(url_for('Admin.home'))
    
    @application.errorhandler(404)
    def handle_not_found(error: exceptions.NotFound) -> str:
        return render_template('404.html')
    
    @application.get('/assets/<path:filename>')
    def instance_asset(filename: str) -> Response:
        directory = os.path.join(application.instance_path, assets_dir)
        return send_from_directory(directory=directory, path=filename, as_attachment=False)

    @application.context_processor
    def admin_template_context_processor() -> dict[str, Any]:
        def raise_error(msg: str) -> NoReturn:
            raise TemplateError(msg)
        return dict(raise_error=raise_error)

    click.echo(click.style(title, fg='bright_cyan'))
    return application


@click.group(cls=FlaskGroup, create_app=make_app)
def cli() -> None:
    """The CLI to manage frolic webserver."""


class FlashCategory(StrEnum):
    PRIMARY = auto()
    SECONDARY = auto()
    SUCCESS = auto()
    DANGER = auto()
    WARNING = auto()
    INFO = auto()
    LIGHT = auto()
    DARK = auto()