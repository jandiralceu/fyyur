from datetime import datetime
from json import dumps, loads
from flask import flash, redirect, request, render_template, url_for, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from forms import ArtistForm
from models.artist import Artist
from models.show import Show

blp = Blueprint('artists', __name__)


@blp.route('/', methods=['GET'])
def artists():
    data = Artist.query.order_by(Artist.id.desc()).all()
    return render_template('pages/artists.html', artists=data)


@blp.route('/search', methods=['POST'])
def search_artists():
    """This function handles the HTTP POST request to search for artists."""
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

    return render_template(
        'pages/search_artists.html', 
        results={"count": len(artists), "data": artists}, 
        search_term=search_term
    )

    
@blp.route('/<int:artist_id>')
def show_artist(artist_id: int):
    """This function handles the HTTP GET request to show an artist."""
    
    artist_data = db.session.query(
        Artist,
        Show
    ).outerjoin(Show).filter(Artist.id == artist_id).all()
    
    if not artist_data:
        flash('Details for artist with ID ' + str(artist_id) + ' could not be found.', 'error')
        return redirect(url_for('artists.artists'))
    
    current_time = datetime.now()
    upcoming_shows = []
    past_shows = []
    
    for _, show in artist_data:
        if hasattr(show, 'start_time'):
            if show.start_time > current_time:
                upcoming_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.venue.name,
                    "venue_image_link": show.venue.image_link,
                    "start_time": show.start_time
                })
            else:
                past_shows.append({
                    "venue_id": show.venue_id,
                    "venue_name": show.venue.name,
                    "venue_image_link": show.venue.image_link,
                    "start_time": show.start_time
                })
    
    
    artist_info = artist_data[0][0]
    
    artist = {
        "id": artist_info.id,
        "name": artist_info.name,
        "city": artist_info.city,
        "state": artist_info.state,
        "phone": artist_info.phone,
        "genres": loads(artist_info.genres),
        "image_link": artist_info.image_link,
        "facebook_link": artist_info.facebook_link,
        "website": artist_info.website_link,
        "seeking_venue": artist_info.seeking_venue,
        "seeking_description": artist_info.seeking_description,
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows": past_shows,
        "past_shows_count": len(past_shows)
    }
    
    return render_template('pages/show_artist.html', artist=artist)
    

@blp.route('/create', methods=['GET'])
def create_artist_form():
    """This function handles the HTTP GET request to show the create artist form."""
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@blp.route('/create', methods=['POST'])
def create_artist_submission():
    """This function handles the HTTP POST request to create a new artist."""
    try:
        artist = Artist(
            name=request.form["name"],
            city=request.form["city"],
            state=request.form["state"],
            phone=request.form["phone"],
            genres=dumps(request.form.getlist('genres')),
            image_link=request.form["image_link"],
            facebook_link=request.form["facebook_link"],
            website_link=request.form["website_link"],
            seeking_venue="seeking_venue" in request.form,
            seeking_description=request.form["seeking_description"],
        )
        
        db.session.add(artist)
        db.session.commit()
        
        flash('Artist ' + artist.name + ' was successfully listed!')
    except SQLAlchemyError as _:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', 'error')
    
    return render_template('pages/home.html')
    

@blp.route('/<string:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id: str):
    """edit_artist returns the update artist form."""
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)
    
    for key in form.data:
        if hasattr(artist, key):
            form[key].default = artist.__dict__[key] if key != 'genres' else loads(artist.genres)
    
    form.process()

    return render_template('forms/edit_artist.html', form=form, artist=artist)
    

@blp.route('/<string:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id: str):
    """This function handles the HTTP GET request to edit an artist."""
    artist: Artist = Artist.query.get_or_404(artist_id)
    # Update the seeking_venue attribute first cause this property is not included in the form when it's not checked
    artist.seeking_venue = "seeking_venue" in request.form
    
    for key in request.form:
        if hasattr(artist, key):
            match key:
                case 'genres':
                    setattr(artist, key, dumps(request.form.getlist('genres')))
                case 'seeking_venue':
                    continue
                case _:
                    setattr(artist, key, request.form[key])
    
    db.session.commit()
    
    return redirect(url_for('artists.show_artist', artist_id=artist_id))