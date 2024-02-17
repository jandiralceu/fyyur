import sys
from flask import (Blueprint, flash, render_template, request)
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
    form = ShowForm(request.form)
    show = Show()
    form.populate_obj(show)
    
    artist = Artist.query.get_or_404(show.artist_id)
    venue = Venue.query.get_or_404(show.venue_id)
    
    if artist is None:
      flash('Unable to find artist with ID: ' + show.artist_id, 'error')
      return render_template('forms/new_show.html', form=ShowForm())
    
    if venue is None:
      flash('Unable to find venue with ID: ' + show.venue_id, 'error')
      return render_template('forms/new_show.html', form=ShowForm())
    
    if not artist.seeking_venue:
      flash('Artist is not accepting shows at the moment.', 'error')
      return render_template('forms/new_show.html', form=ShowForm())
    
    if not venue.seeking_talent:
      flash('Venue is not accepting shows at the moment.', 'error')
      return render_template('forms/new_show.html', form=ShowForm())
    
    if show.start_time < datetime.now():
      flash('Show time cannot be in the past.', 'error')
      return render_template('forms/new_show.html', form=ShowForm())
    
    db.session.add(show)
    db.session.commit()
    
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  except SQLAlchemyError as _:
    print(sys.exc_info())
    db.session.rollback()
    
    flash('An error occurred. Show could not be listed.', 'error')
    return render_template('forms/new_show.html', form=ShowForm())
  except ValueError as e:
    print(sys.exc_info())
    db.session.rollback()
    
    flash('An error ocurred. Please check the form data and try again.', 'error')
    return render_template('forms/new_show.html', form=ShowForm())
  finally:
    db.session.close()
