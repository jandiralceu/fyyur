from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate
import logging

from db import db
from helpers import filters


def create_app():
    app = Flask(__name__)
    moment = Moment(app)

    app.config.from_object('config')

    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)

    app.jinja_env.filters['datetime'] = filters.format_datetime

    @app.route('/')
    def index():
        return render_template('pages/home.html')

    from resources.artists import blp as artist_blueprint
    app.register_blueprint(artist_blueprint, url_prefix='/artists')

    from resources.venues import blp as venue_blueprint
    app.register_blueprint(venue_blueprint, url_prefix='/venues')

    from resources.shows import blp as show_blueprint
    app.register_blueprint(show_blueprint, url_prefix='/shows')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500

    if not app.debug:
        file_handler = logging.FileHandler('error.log')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app
