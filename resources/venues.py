from json import dumps, loads
from flask import flash, redirect, request, render_template, url_for, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from forms import VenueForm
from models.venue import Venue

blp = Blueprint('venues', __name__)


@blp.route('/')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data= Venue.query.all()
    return render_template('pages/venues.html', areas=data);


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
    venue = Venue.query.get_or_404(venue_id)
    venue.genres = loads(venue.genres)
    
    return render_template('pages/show_venue.html', venue=venue)


@blp.route('/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@blp.route('/create', methods=['POST'])
def create_venue_submission():
    try:
        venue = Venue(
            name=request.form["name"],
            city=request.form["city"],
            state=request.form["state"],
            address=request.form["address"],
            phone=request.form["phone"],
            genres=dumps(request.form.getlist('genres')),
            image_link=request.form["image_link"],
            facebook_link=request.form["facebook_link"],
            website_link=request.form["website_link"],
            seeking_talent=hasattr(request.form, "seeking_talent"),
            seeking_description=request.form["seeking_description"]
        )
        
        db.session.add(venue)
        db.session.commit()
        
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except SQLAlchemyError as error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')


@blp.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@blp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)
    
    for key in form.data:
        if hasattr(venue, key):
            form[key].default = venue.__dict__[key] if key != 'genres' else loads(venue.genres)
    
    form.process()
    
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@blp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    # Update the seeking_talent attribute first cause this property is not included in the form when it's not checked
    venue.seeking_talent = hasattr(request.form, "seeking_talent")
    
    for key in request.form:
        if hasattr(venue, key):
            match key:
                case "genres":
                    setattr(venue, key, dumps(request.form.getlist('genres')))
                case "seeking_talent":
                    continue
                case _:
                    setattr(venue, key, request.form[key])
    
    db.session.commit()
            
    return redirect(url_for('venues.show_venue', venue_id=venue_id))
