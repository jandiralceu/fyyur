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
    response={
      "count": 1,
      "data": [{
        "id": 4,
        "name": "Guns N Petals",
        "num_upcoming_shows": 0,
      }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

    
    
    
@blp.route('/<int:artist_id>')
def show_artist(artist_id: int):
    """This function handles the HTTP GET request to show an artist."""
    artist = Artist.query.query.get_or_404(artist_id)
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
            genres=request.form["genres"],
            image_link=request.form["image_link"],
            facebook_link=request.form["facebook_link"],
            website_link=request.form["website_link"],
            seeking_venue=True if request.form["seeking_venue"] == 'y' else False,
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
    """This function handles the HTTP GET request to edit an artist."""
    form = ArtistForm()
    artist = Artist.query.query.get_or_404(artist_id)

    return render_template('forms/edit_artist.html', form=form, artist=artist)
    

@blp.route('/<string:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id: str):
    """This function handles the HTTP GET request to edit an artist."""
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))