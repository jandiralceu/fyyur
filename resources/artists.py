from json import dumps, loads
from flask import flash, redirect, request, render_template, url_for, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from forms import ArtistForm
from models.artist import Artist

blp = Blueprint('artists', __name__)


@blp.route('/', methods=['GET'])
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@blp.route('/search', methods=['POST'])
def search_artists():
    """This function handles the HTTP POST request to search for artists."""
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    
    response = {
      "count": len(artists),
      "data": artists,
    }
    
    return render_template('pages/search_artists.html', results=response, search_term=search_term)

    
@blp.route('/<int:artist_id>')
def show_artist(artist_id: int):
    """This function handles the HTTP GET request to show an artist."""
    artist = Artist.query.get_or_404(artist_id)
    artist.genres = loads(artist.genres)
    
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
            seeking_venue=True if "seeking_venue" in request.form else False,
            seeking_description=request.form["seeking_description"],
        )
        
        db.session.add(artist)
        db.session.commit()
        
        flash('Artist ' + artist.name + ' was successfully listed!')
    except SQLAlchemyError as error:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    
    return render_template('pages/home.html')
    

@blp.route('/<string:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id: str):
    """edit_artist returns the update artist form."""
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)
    
    for key in form.data:
        if key in artist.__dict__:
            if key == 'genres':
                form[key].default = loads(artist.__dict__[key])
            else:
                form[key].default = artist.__dict__[key]
    
    form.process()

    return render_template('forms/edit_artist.html', form=form, artist=artist)
    

@blp.route('/<string:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id: str):
    """This function handles the HTTP GET request to edit an artist."""
    artist = Artist.query.get_or_404(artist_id)
    
    # Update the seeking_venue attribute first cause this property is not in the form when it's not checked
    artist.seeking_venue = True if "seeking_venue" in request.form else False
    
    for key in request.form:
        if key in artist.__dict__:
            if key == 'seeking_venue':
                return
            
            if key == 'genres':
                artist.__dict__[key] = dumps(request.form.getlist('genres'))
                return
            
            artist.__dict__[key] = request.form[key]
    
        
    db.session.add(artist)
    db.session.commit()
    
    return redirect(url_for('artists.show_artist', artist_id=artist_id))