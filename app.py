import dateutil.parser
import babel
from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler


from db import db


def create_app():
  app = Flask(__name__)
  moment = Moment(app)

  app.config.from_object('config')

  db.init_app(app=app)
  
  migrate = Migrate(app, db)
  

  #----------------------------------------------------------------------------#
  # Filters.
  #----------------------------------------------------------------------------#

  def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

  app.jinja_env.filters['datetime'] = format_datetime


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
      file_handler = FileHandler('error.log')
      file_handler.setFormatter(
          Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
      )
      app.logger.setLevel(logging.INFO)
      file_handler.setLevel(logging.INFO)
      app.logger.addHandler(file_handler)
      app.logger.info('errors')


  return app

