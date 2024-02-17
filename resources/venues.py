from datetime import datetime
from json import dumps, loads
import sys
from flask import (flash, redirect, request, render_template, url_for, Blueprint)
from sqlalchemy.exc import SQLAlchemyError

from db import db
from forms import VenueForm
from models.venue import Venue
from models.show import Show

blp = Blueprint('venues', __name__)


@blp.route('/')
def venues():
    venues_data = Venue.query.order_by(Venue.city, Venue.state).all()
    
    areas_data = {}
    
    for venue in venues_data:
        area_key = (venue.city, venue.state)
        if area_key not in areas_data:
            areas_data[area_key] = {
                "city": venue.city,
                "state": venue.state,
                "venues": []
            }
            
        areas_data[area_key]["venues"].append({
            "id": venue.id,
            "name": venue.name,
        })
    
    
    areas = [{
        'city': area['city'], 
        'state': area['state'], 
        'venues': area['venues']
    } for area in areas_data.values()]
        
    return render_template('pages/venues.html', areas=areas);


@blp.route('/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

    return render_template(
        'pages/search_venues.html', 
        results={"count": len(venues), "data": venues}, 
        search_term=search_term)


@blp.route('/<int:venue_id>')
def show_venue(venue_id):
    venues_data = db.session.query(
        Venue,
        Show
    ).outerjoin(Show).filter(Venue.id == venue_id).all()
    
    if not venues_data:
        flash('Details for venue with ID ' + str(venue_id) + ' could not be found.', 'error')
        return redirect(url_for('venues.venues'))
    
    current_time = datetime.now()
    upcoming_shows = []
    past_shows = []
    
    for _, show in venues_data:
        if hasattr(show, 'start_time'):
            if show.start_time > current_time:
                upcoming_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                })
            else:
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                })
    
    (data, _) = venues_data[0]
    genres = loads(data.genres)
    # print(data.genres)
    
    venue = {
        "id": data.id,
        "name": data.name,
        "genres": genres,  
        "address": data.address,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "website": data.website_link,
        "facebook_link": data.facebook_link,
        "seeking_talent": data.seeking_talent,
        "seeking_description": data.seeking_description,
        "image_link": data.image_link,
        "upcoming_shows": upcoming_shows,
        "past_shows": past_shows,
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows_count": len(past_shows)
    }
    
    return render_template('pages/show_venue.html', venue=venue)


@blp.route('/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@blp.route('/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    
    try:
        venue = Venue()
        form.populate_obj(venue)
        
        if not form.validate():
            return render_template('forms/new_venue.html', form=form)
        
        venue.genres = dumps(request.form.getlist('genres'))
    
        db.session.add(venue)
        db.session.commit()
        
        flash('Venue ' + venue.name + ' was successfully listed!')
        return redirect('/')
    except SQLAlchemyError as _:
        print(sys.exc_info())
        db.session.rollback()
        
        flash('An error occurred. Venue ' + form.name + ' could not be created.', 'error')
        return render_template('forms/new_venue.html', form=VenueForm())
    except ValueError as e:
        print(sys.exc_info())
        db.session.rollback()
        
        flash('An error ocurred. Please check the form data and try again.', 'error')
        return render_template('forms/new_venue.html', form=VenueForm())
    finally:
        db.session.close()



@blp.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    '''Delete a venue by its ID. This will also delete all shows associated with the venue.'''
    try:
        venue = Venue.query.get_or_404(venue_id)
        
        for show in venue.shows:
            db.session.delete(show)
    
        db.session.delete(venue)
        db.session.commit()
        
        flash('Venue ' + venue.name + ' was successfully deleted!')
    except SQLAlchemyError as _:
        flash('Unable to delete the selected venue, please try again later!', 'error')
    
    return redirect('/')



@blp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    '''Edit venue by its ID. It will pre-populate the form with the venue data.'''
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm()
    
    for key in form.data:
        if hasattr(venue, key):
            if key == 'genres':
                form[key].default = loads(venue.genres)
            else:
                form[key].default = venue.__dict__[key]
    
    form.process()
    
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@blp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    '''Edit venue by its ID. It will update the venue data with the form data.'''
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(request.form)
    
    form.populate_obj(venue)
    
    try:
        if not form.validate():
            return render_template('forms/edit_venue.html', form=form, venue=venue)
        
        venue.genres = dumps(venue.genres)
        db.session.commit()
        
        return redirect(url_for('venues.show_venue', venue_id=venue_id))
    except SQLAlchemyError as _:
        print(sys.exc_info())
        db.session.rollback()
        
        flash('An error occurred. Venue ' + form.name + ' could not be updated.', 'error')
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    except ValueError as e:
        print(sys.exc_info())
        db.session.rollback()
        
        flash('An error ocurred. Please check the form data and try again.', 'error')
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    finally:
        db.session.close()
        
            
    
