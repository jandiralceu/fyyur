from flask import Blueprint, flash, render_template, request
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from db import db

from forms import ShowForm
from models.show import Show
from models.artist import Artist
from models.venue import Venue

blp = Blueprint('shows', __name__)


@blp.route('/shows')
def shows():
    shows = db.session.query(
      Show.start_time,
      Show.venue_id,
      Venue.name.label('venue_name'),
      Show.artist_id,
      Artist.name.label('artist_name'),
      Artist.image_link.label('artist_image_link')).join(Artist).join(Venue).all()
    
    return render_template('pages/shows.html', shows=shows)


@blp.route('/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@blp.route('/create', methods=['POST'])
def create_show_submission():
  try:
    show = Show(
      artist_id=int(request.form['artist_id']),
      venue_id=int(request.form['venue_id']),
      start_time=datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
    )
    
    db.session.add(show)
    db.session.commit()
    
    flash('Show was successfully listed!')
  except SQLAlchemyError as _:
    flash('An error occurred. Show could not be listed.', 'error')

  return render_template('pages/home.html')