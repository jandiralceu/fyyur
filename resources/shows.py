import logging

from flask import (Blueprint, flash, render_template, request)
from sqlalchemy.exc import SQLAlchemyError
from wtforms import ValidationError

from db import db

from forms import ShowForm
from models.show import Show
from models.artist import Artist
from models.venue import Venue

blp = Blueprint('shows', __name__)


@blp.route('/shows')
def shows():
    """This function handles the HTTP GET request to show all shows."""
    result = db.session.query(
        Show.start_time,
        Show.venue_id,
        Venue.name.label('venue_name'),
        Show.artist_id,
        Artist.name.label('artist_name'),
        Artist.image_link.label('artist_image_link')).join(Artist).join(Venue).all()

    return render_template('pages/shows.html', shows=result)


@blp.route('/create')
def create_shows():
    """This function handles the HTTP GET request to create a new show form."""
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@blp.route('/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    try:
        show = Show()
        form.populate_obj(show)

        if not form.validate():
            return render_template('forms/new_show.html', form=form)

        artist = Artist.query.filter_by(id=show.artist_id).first()
        venue = Venue.query.filter_by(id=show.venue_id).first()

        if artist is None:
            raise ValidationError(f'Unable to find artist with ID: {show.artist_id}')

        if venue is None:
            raise ValidationError(f'Unable to find venue with ID: {show.venue_id}')

        if artist and not artist.seeking_venue:
            raise ValidationError('The selected artist is not accepting shows at the moment.')

        if venue and not venue.seeking_talent:
            raise ValidationError('The selected venue is not accepting shows at the moment.')

        if not form.validate():
            return render_template('forms/new_show.html', form=form)

        db.session.add(show)
        db.session.commit()

        flash('Show was successfully listed!')
        return render_template('pages/home.html')
    except SQLAlchemyError as e:
        logging.error(e)
        db.session.rollback()

        flash('An error occurred. Show could not be created.', 'error')
        return render_template('forms/new_show.html', form=form)
    except ValueError as e:
        logging.error(e)
        db.session.rollback()

        flash(e, category='error')
        return render_template('forms/new_show.html', form=form)
    finally:
        db.session.close()
